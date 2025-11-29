from sqlalchemy import text, func
from src.utils.db_session import get_db_session
from src.model.scraping_models import ScrapedPage, ScrapedArticle, ScrapingError


class ScrapingReportsService:
    """
    Gera relatórios e estatísticas sobre os dados coletados via scraping.
    Utiliza consultas SQL com operações de JOIN e agregações.
    """

    @staticmethod
    def get_pages_with_articles():
        """
        Relatório com INNER JOIN: Retorna páginas que possuem artigos extraídos.
        Agrupa por página e conta o número de artigos.

        Returns:
            Result: Objeto Result do SQLAlchemy ou None em caso de erro.
        """
        query = text(
            """
            SELECT 
                sp.id_page,
                sp.url,
                sp.title AS page_title,
                sp.scraping_date,
                COUNT(sa.id_article) AS articles_count
            FROM scraped_page sp
            INNER JOIN scraped_article sa ON sp.id_page = sa.page_id_fk
            GROUP BY sp.id_page, sp.url, sp.title, sp.scraping_date
            ORDER BY articles_count DESC;
        """
        )

        db = get_db_session()
        try:
            return db.execute(query)
        except Exception as e:
            print(f"Erro no relatório INNER JOIN: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_pages_with_errors():
        """
        Relatório com LEFT JOIN: Retorna todas as páginas e seus erros (se houver).
        Páginas sem erros também são incluídas com contagem 0.

        Returns:
            Result: Objeto Result do SQLAlchemy ou None em caso de erro.
        """
        query = text(
            """
            SELECT 
                sp.url,
                sp.title,
                sp.status_code,
                COUNT(se.id_error) AS error_count,
                STRING_AGG(DISTINCT se.error_type, ', ') AS error_types
            FROM scraped_page sp
            LEFT JOIN scraping_error se ON sp.id_page = se.page_id_fk
            GROUP BY sp.id_page, sp.url, sp.title, sp.status_code
            ORDER BY error_count DESC;
        """
        )

        db = get_db_session()
        try:
            return db.execute(query)
        except Exception as e:
            print(f"Erro no relatório LEFT JOIN: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_all_errors_with_pages():
        """
        Relatório simulando RIGHT JOIN: Retorna todos os erros e suas páginas associadas.
        Erros sem página associada também são incluídos.

        Returns:
            Result: Objeto Result do SQLAlchemy ou None em caso de erro.
        """
        query = text(
            """
            SELECT 
                se.id_error,
                se.url_attempted,
                se.error_type,
                se.error_message,
                se.occurred_at,
                sp.url AS page_url,
                sp.title AS page_title
            FROM scraping_error se
            LEFT JOIN scraped_page sp ON se.page_id_fk = sp.id_page
            ORDER BY se.occurred_at DESC;
        """
        )

        db = get_db_session()
        try:
            return db.execute(query)
        except Exception as e:
            print(f"Erro no relatório de erros: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_summary_statistics():
        """
        Calcula estatísticas gerais do scraping.

        Returns:
            dict: Dicionário com total_pages, total_articles, total_errors e avg_articles_per_page.
                  Retorna None em caso de erro.
        """
        db = get_db_session()
        try:
            total_pages = db.query(func.count(ScrapedPage.id_page)).scalar()
            total_articles = db.query(func.count(ScrapedArticle.id_article)).scalar()
            total_errors = db.query(func.count(ScrapingError.id_error)).scalar()

            # Calcula média de artigos por página
            avg_articles_per_page = db.query(
                func.avg(
                    db.query(func.count(ScrapedArticle.id_article))
                    .filter(ScrapedArticle.page_id_fk == ScrapedPage.id_page)
                    .correlate(ScrapedPage)
                    .scalar_subquery()
                )
            ).scalar()

            return {
                "total_pages": total_pages or 0,
                "total_articles": total_articles or 0,
                "total_errors": total_errors or 0,
                "avg_articles_per_page": float(avg_articles_per_page or 0),
            }
        except Exception as e:
            print(f"Erro nas estatísticas: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def get_articles_by_author():
        """
        Relatório: Agrupa artigos por autor e conta quantos artigos cada um escreveu.
        Exclui autores "Unknown" e limita aos top 20.

        Returns:
            Result: Objeto Result do SQLAlchemy ou None em caso de erro.
        """
        query = text(
            """
            SELECT 
                sa.author,
                COUNT(sa.id_article) AS article_count,
                STRING_AGG(DISTINCT sp.url, ' | ') AS sources
            FROM scraped_article sa
            INNER JOIN scraped_page sp ON sa.page_id_fk = sp.id_page
            WHERE sa.author != 'Unknown'
            GROUP BY sa.author
            HAVING COUNT(sa.id_article) > 0
            ORDER BY article_count DESC
            LIMIT 20;
        """
        )

        db = get_db_session()
        try:
            return db.execute(query)
        except Exception as e:
            print(f"Erro no relatório por autor: {e}")
            return None
        finally:
            db.close()
