import sys
from src.utils.db_session import check_db_connection, init_db
from src.service.scraping_service import WebScrapingService
from src.service.scraping_reports_service import ScrapingReportsService


def print_separator(title: str = ""):
    """
    Imprime um separador visual no console.

    Args:
        title (str): Título a ser exibido no separador (opcional).
    """
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print("=" * 70)
    else:
        print("-" * 70)


def execute_scraping():
    """
    Executa o processo de web scraping em múltiplas URLs.
    Exibe estatísticas de sucesso e falha ao final.
    """
    print_separator("WEB SCRAPING - COLETA DE DADOS")

    # URLs de exemplo - modifique conforme necessário
    urls_to_scrape = [
        "https://realpython.com/",
        "https://dev.to/",
        "https://medium.com/tag/python",
        "https://news.ycombinator.com/",
    ]

    print("\nURLs configuradas para scraping:")
    for idx, url in enumerate(urls_to_scrape, 1):
        print(f"  {idx}. {url}")

    print("\nIniciando processo de scraping...")
    print_separator()

    scraper = WebScrapingService()
    stats = scraper.scrape_multiple_urls(urls_to_scrape)

    print_separator("RESULTADO DO SCRAPING")
    print(f"Total de URLs processadas: {stats['total']}")
    print(f"Sucessos: {stats['success']}")
    print(f"Falhas: {stats['failed']}")

    if stats["failed_urls"]:
        print("\nURLs que falharam:")
        for url in stats["failed_urls"]:
            print(f"  - {url}")


def generate_reports():
    """
    Gera e exibe relatórios dos dados coletados via scraping.
    Inclui estatísticas gerais e consultas SQL com JOINs.
    """
    print_separator("RELATÓRIOS DO WEB SCRAPING")

    reports = ScrapingReportsService()

    # Estatísticas gerais
    print("\n[1] ESTATÍSTICAS GERAIS")
    print_separator()
    stats = reports.get_summary_statistics()
    if stats:
        print(f"Total de páginas processadas: {stats['total_pages']}")
        print(f"Total de artigos extraídos: {stats['total_articles']}")
        print(f"Total de erros registrados: {stats['total_errors']}")
        print(f"Média de artigos por página: {stats['avg_articles_per_page']:.2f}")

    # Páginas com artigos (INNER JOIN)
    print("\n[2] PÁGINAS COM ARTIGOS (INNER JOIN)")
    print_separator()
    result = reports.get_pages_with_articles()
    if result:
        rows = result.mappings().all()
        if rows:
            for row in rows:
                print(f"\nPágina: {row['page_title']}")
                print(f"  URL: {row['url']}")
                print(f"  Artigos extraídos: {row['articles_count']}")
                print(f"  Data scraping: {row['scraping_date']}")
        else:
            print("Nenhum dado encontrado.")

    # Páginas com erros (LEFT JOIN)
    print("\n[3] PÁGINAS E ERROS (LEFT JOIN)")
    print_separator()
    result = reports.get_pages_with_errors()
    if result:
        rows = result.mappings().all()
        if rows:
            for row in rows:
                print(f"\nURL: {row['url']}")
                print(f"  Status: {row['status_code']}")
                print(f"  Erros: {row['error_count']}")
                if row["error_types"]:
                    print(f"  Tipos: {row['error_types']}")
        else:
            print("Nenhum dado encontrado.")

    # Todos os erros
    print("\n[4] HISTÓRICO DE ERROS")
    print_separator()
    result = reports.get_all_errors_with_pages()
    if result:
        rows = result.mappings().all()
        if rows:
            for row in rows[:10]:  # Limita a 10 erros mais recentes
                print(f"\nErro #{row['id_error']}")
                print(f"  URL tentada: {row['url_attempted']}")
                print(f"  Tipo: {row['error_type']}")
                print(f"  Mensagem: {row['error_message'][:100]}...")
                print(f"  Ocorreu em: {row['occurred_at']}")
        else:
            print("Nenhum erro registrado.")

    # Artigos por autor
    print("\n[5] ARTIGOS POR AUTOR")
    print_separator()
    result = reports.get_articles_by_author()
    if result:
        rows = result.mappings().all()
        if rows:
            for idx, row in enumerate(rows, 1):
                print(f"{idx}. {row['author']}: {row['article_count']} artigos")
        else:
            print("Nenhum autor encontrado.")


def main():
    """
    Função principal que executa o menu interativo do módulo de scraping.
    Verifica a conexão com o banco antes de iniciar.
    """

    if not check_db_connection():
        sys.exit(1)

    init_db()

    print("\n" + "=" * 70)
    print("  TASKFY - WEB SCRAPING MODULE (TP5)")
    print("=" * 70)

    while True:
        print("\nOpções:")
        print("  1. Executar Web Scraping")
        print("  2. Gerar Relatórios")
        print("  3. Executar Scraping + Relatórios")
        print("  0. Sair")
        print_separator()

        choice = input("Escolha uma opção: ").strip()

        if choice == "1":
            execute_scraping()
        elif choice == "2":
            generate_reports()
        elif choice == "3":
            execute_scraping()
            generate_reports()
        elif choice == "0":
            print("\nEncerrando. Até mais!")
            break
        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    main()
