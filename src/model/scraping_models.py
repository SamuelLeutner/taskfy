from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class ScrapedPage(Base):
    """
    Representa uma página web visitada durante o scraping.
    Esta classe será mapeada para a tabela "scraped_page".

    Attributes:
        id_page (int): O identificador único da página (Chave Primária).
        url (str): A URL completa da página visitada.
        title (str): O título extraído da tag <title> da página.
        scraping_date (datetime): A data e hora em que o scraping foi realizado.
        status_code (int): O código HTTP da resposta (ex: 200, 404, 500).
        content_length (int): O tamanho do conteúdo HTML em bytes.
    """

    __tablename__ = "scraped_page"

    id_page = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False, unique=True)
    title = Column(String(255))
    scraping_date = Column(TIMESTAMP, server_default=func.now())
    status_code = Column(Integer)
    content_length = Column(Integer)

    articles = relationship("ScrapedArticle", back_populates="page")
    errors = relationship("ScrapingError", back_populates="page")

    def __str__(self):
        """Retorna uma representação amigável da página em string."""
        return f"ID: {self.id_page} | URL: {self.url} | Status: {self.status_code}"


class ScrapedArticle(Base):
    """
    Representa um artigo/conteúdo extraído de uma página web.
    Esta classe será mapeada para a tabela "scraped_article".

    Attributes:
        id_article (int): O identificador único do artigo (Chave Primária).
        page_id_fk (int): Chave estrangeira para a página de origem.
        title (str): O título do artigo extraído.
        author (str): O nome do autor do artigo.
        publish_date (str): A data de publicação do artigo (formato texto).
        content_preview (str): Um preview/resumo do conteúdo do artigo.
        article_url (str): A URL específica do artigo (se diferente da página).
        extraction_date (datetime): A data e hora em que os dados foram extraídos.
    """

    __tablename__ = "scraped_article"

    id_article = Column(Integer, primary_key=True)
    page_id_fk = Column(Integer, ForeignKey("scraped_page.id_page"), nullable=False)
    title = Column(String(255))
    author = Column(String(100))
    publish_date = Column(String(50))
    content_preview = Column(Text)
    article_url = Column(String(500))
    extraction_date = Column(TIMESTAMP, server_default=func.now())

    page = relationship("ScrapedPage", back_populates="articles")

    def __str__(self):
        """Retorna uma representação amigável do artigo em string."""
        return f"ID: {self.id_article} | Título: {self.title} | Autor: {self.author}"


class ScrapingError(Base):
    """
    Representa um erro ocorrido durante o processo de scraping.
    Esta classe será mapeada para a tabela "scraping_error".

    Attributes:
        id_error (int): O identificador único do erro (Chave Primária).
        page_id_fk (int): Chave estrangeira para a página (se aplicável).
        url_attempted (str): A URL que estava sendo acessada quando o erro ocorreu.
        error_type (str): O tipo/classe da exceção (ex: HTTPError, URLError).
        error_message (str): A mensagem detalhada do erro.
        occurred_at (datetime): A data e hora em que o erro ocorreu.
    """

    __tablename__ = "scraping_error"

    id_error = Column(Integer, primary_key=True)
    page_id_fk = Column(Integer, ForeignKey("scraped_page.id_page"), nullable=True)
    url_attempted = Column(String(500), nullable=False)
    error_type = Column(String(100))
    error_message = Column(Text)
    occurred_at = Column(TIMESTAMP, server_default=func.now())

    page = relationship("ScrapedPage", back_populates="errors")

    def __str__(self):
        """Retorna uma representação amigável do erro em string."""
        return (
            f"ID: {self.id_error} | Tipo: {self.error_type} | URL: {self.url_attempted}"
        )
