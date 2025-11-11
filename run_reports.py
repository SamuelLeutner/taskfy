from src.service.reports_service import (
    get_inner_join_report,
    get_left_join_report,
    get_right_join_report
)
from src.utils.db_session import check_db_connection, init_db
import sys

def print_results(report_name: str, query_function):
    """
    Função auxiliar que executa uma consulta e imprime os resultados
    como Dicionários (Etapas 5, 6) e Listas (Etapas 7, 8).
    
    Argumentos:
        report_name (str): O título a ser impresso para o relatório.
        query_function (function): A função do serviço que executa a query.
    """
    
    print(f"\n--- {report_name} (Resultado como DICIONÁRIO) [Etapas 5 e 6] ---")
    
    db_result_dict = query_function()
    if db_result_dict is None:
        print("Erro ao executar consulta (dicionário).")
        return
    
    results_dict = db_result_dict.mappings().all()
    
    if not results_dict:
        print("Nenhum resultado encontrado.")
    else:
        for item in results_dict:
            print(dict(item)) 
            
    db_result_dict.close() 
    
    print(f"\n--- {report_name} (Resultado como LISTA) [Etapas 7 e 8] ---")
    
    db_result_list = query_function()
    if db_result_list is None:
        print("Erro ao executar consulta (lista).")
        return
    
    results_list = db_result_list.all()
    
    if not results_list:
        print("Nenhum resultado encontrado.")
    else:
        for item in results_list:
            print(item) 
            
    db_result_list.close() 

def main():
    """Função principal que orquestra a execução dos relatórios."""
    
    if not check_db_connection():
        sys.exit(1) 
    
    init_db() 
    
    print("\nExecutando requisitos do TP3 - Taskfy (Relatórios)")
    print("="*50)
    
    print_results("Relatório 1: INNER JOIN (Tarefas Pendentes)", get_inner_join_report)
    print_results("Relatório 2: LEFT JOIN (Tarefas por Categoria)", get_left_join_report)
    print_results("Relatório 3: RIGHT JOIN (Usuários e suas Tarefas)", get_right_join_report)

if __name__ == "__main__":
    main()