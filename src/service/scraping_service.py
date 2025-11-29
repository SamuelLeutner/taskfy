import re
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from src.model.scraping_models import ScrapedPage, ScrapedArticle, ScrapingError
from src.utils.db_session import get_db_session


class WebScrapingService:
    """
    Serviço responsável por realizar web crawling e web scraping.
    Utiliza urllib para download de páginas e BeautifulSoup para parsing HTML.
    """

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def __init__(self):
        """Inicializa o serviço de scraping."""
        self.db = None

    def _get_html_content(self, url: str) -> tuple[str, int]:
        """
        Baixa o conteúdo HTML de uma URL utilizando urllib.

        Args:
            url (str): A URL a ser acessada.

        Returns:
            tuple[str, int]: Uma tupla contendo (html_content, status_code).

        Raises:
            Exception: Se houver erro no download (HTTP, URL ou inesperado).
        """
        req = Request(url, headers={"User-Agent": self.USER_AGENT})

        try:
            with urlopen(req, timeout=10) as response:
                html = response.read().decode("utf-8")
                return html, response.status
        except HTTPError as e:
            raise Exception(f"HTTP Error {e.code}: {e.reason}")
        except URLError as e:
            raise Exception(f"URL Error: {e.reason}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")

    def _extract_articles(self, soup: BeautifulSoup, url: str) -> list[dict]:
        """
        Extrai informações de artigos/posts da página HTML parseada.
        Utiliza seletores CSS e expressões regulares para localizar elementos.

        Args:
            soup (BeautifulSoup): Objeto BeautifulSoup com o HTML parseado.
            url (str): URL da página (usado para resolver links relativos).

        Returns:
            list[dict]: Lista de dicionários contendo os dados extraídos de cada artigo.
        """
        articles = []

        # Busca por elementos article ou divs com classes relacionadas a posts
        article_tags = soup.find_all(
            ["article", "div"], class_=re.compile(r"(post|article|entry|item)", re.I)
        )

        if not article_tags:
            # Fallback: tenta encontrar divs/sections com classes
            article_tags = soup.find_all(["div", "section"], class_=True)[:10]

        for idx, article in enumerate(article_tags[:20]):  # Limita a 20 artigos
            try:
                # Extrai título
                title_tag = article.find(["h1", "h2", "h3", "h4"])
                title = (
                    title_tag.get_text(strip=True)
                    if title_tag
                    else f"Untitled Article {idx+1}"
                )

                # Extrai autor
                author_tag = article.find(
                    ["span", "div", "a"], class_=re.compile(r"author", re.I)
                )
                author = author_tag.get_text(strip=True) if author_tag else "Unknown"

                # Extrai data de publicação
                date_tag = article.find(
                    ["time", "span"], class_=re.compile(r"(date|time|published)", re.I)
                )
                publish_date = date_tag.get_text(strip=True) if date_tag else "N/A"

                # Extrai preview do conteúdo
                content_tag = article.find(
                    ["p", "div"],
                    class_=re.compile(r"(content|excerpt|description)", re.I),
                )
                content_preview = (
                    content_tag.get_text(strip=True)[:500] if content_tag else ""
                )

                # Extrai URL do artigo
                link_tag = article.find("a", href=True)
                article_url = link_tag["href"] if link_tag else ""
                if article_url and not article_url.startswith("http"):
                    from urllib.parse import urljoin

                    article_url = urljoin(url, article_url)

                articles.append(
                    {
                        "title": title,
                        "author": author,
                        "publish_date": publish_date,
                        "content_preview": content_preview,
                        "article_url": article_url,
                    }
                )
            except Exception as e:
                print(f"Erro ao extrair artigo {idx}: {e}")
                continue

        return articles

    def scrape_url(self, url: str) -> bool:
        """
        Executa o scraping completo de uma URL.
        Baixa o HTML, extrai dados e armazena no banco de dados.

        Args:
            url (str): A URL a ser processada.

        Returns:
            bool: True se o scraping foi bem-sucedido, False caso contrário.
        """
        self.db = get_db_session()

        try:
            # Verifica se a URL já foi processada
            existing_page = (
                self.db.query(ScrapedPage).filter(ScrapedPage.url == url).first()
            )
            if existing_page:
                print(f"URL já processada: {url}")
                return True

            # Baixa o conteúdo HTML
            print(f"Baixando: {url}")
            html_content, status_code = self._get_html_content(url)

            # Parse do HTML com BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            page_title = soup.find("title")
            page_title = page_title.get_text(strip=True) if page_title else "No Title"

            # Salva metadados da página no banco
            scraped_page = ScrapedPage(
                url=url,
                title=page_title,
                status_code=status_code,
                content_length=len(html_content),
            )
            self.db.add(scraped_page)
            self.db.flush()  # Obtém o ID gerado

            # Extrai artigos da página
            print(f"Extraindo artigos de: {url}")
            articles_data = self._extract_articles(soup, url)

            # Salva cada artigo no banco
            for article_data in articles_data:
                article = ScrapedArticle(
                    page_id_fk=scraped_page.id_page, **article_data
                )
                self.db.add(article)

            self.db.commit()
            print(f"Sucesso! {len(articles_data)} artigos extraídos de {url}")
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Erro ao processar {url}: {e}")

            # Registra o erro no banco
            try:
                error = ScrapingError(
                    url_attempted=url, error_type=type(e).__name__, error_message=str(e)
                )
                self.db.add(error)
                self.db.commit()
            except:
                pass

            return False

        finally:
            if self.db:
                self.db.close()

    def scrape_multiple_urls(self, urls: list[str]) -> dict:
        """
        Realiza scraping de múltiplas URLs em sequência.

        Args:
            urls (list[str]): Lista de URLs a serem processadas.

        Returns:
            dict: Dicionário com estatísticas do processo (total, success, failed, failed_urls).
        """
        stats = {"total": len(urls), "success": 0, "failed": 0, "failed_urls": []}

        for url in urls:
            if self.scrape_url(url):
                stats["success"] += 1
            else:
                stats["failed"] += 1
                stats["failed_urls"].append(url)

        return stats
