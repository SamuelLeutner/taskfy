import sys
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from src.utils.menu import print_menu
from src.service.task_service import TaskService
from src.utils.db_session import init_db, get_db_session, DB_HOST, DB_NAME, DB_USER


def check_db_connection():
    """Verifica se a conexão com o banco de dados pode ser estabelecida."""
    print("Verificando conexão com o banco de dados...")
    try:
        db = get_db_session()
        db.execute(text("SELECT 1"))
        db.close()
        print(f"Conexão com o banco de dados bem-sucedida (Banco: {DB_NAME})")
        return True
    except OperationalError:
        print("\n" + "=" * 50)
        print(f"ERRO FATAL: Não foi possível conectar ao banco de dados.")
        print("1. O servidor PostgreSQL está rodando?")
        print(f"2. As credenciais no arquivo .env estão corretas?")
        print(f"   (Host: {DB_HOST}, Banco: {DB_NAME}, Usuário: {DB_USER})")
        print("=" * 50 + "\n")
        return False
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")
        return False


def main():
    """
    Função principal que executa o loop do menu interativo.
    Esta função é responsável por toda a interação com o usuário.
    """

    if not check_db_connection():
        sys.exit("Encerrando aplicação. Verifique a conexão com o banco.")

    init_db()

    task_service = TaskService()

    while True:
        print_menu()
        choice = input("Escolha uma opção: ")

        if choice == "1":
            description = input("Digite a descrição da nova tarefa: ")
            try:

                user_id = int(input("Digite o ID do usuário (ex: 1 para Alice): "))
                category_id = int(
                    input("Digite o ID da categoria (ex: 1 para Trabalho): ")
                )
            except ValueError:
                print("ID inválido. Usando IDs padrão (1, 1).")
                user_id = 1
                category_id = 1

            added_task = task_service.add_task(description, user_id, category_id)
            if added_task:

                print(f"\nSucesso! Tarefa adicionada:")
                print(added_task)
            else:
                print("Erro ao adicionar tarefa.")

        elif choice == "2":
            print("\n--- Tarefas Pendentes ---")
            pending_tasks = task_service.list_pending_tasks()

            if not pending_tasks:
                print("Nenhuma tarefa pendente no momento.")
            else:
                for task in pending_tasks:
                    print(task)

        elif choice == "3":
            print("\n--- Todas as Tarefas (Pendentes e Concluídas) ---")
            all_tasks = task_service.list_all_tasks()

            if not all_tasks:
                print("Nenhuma tarefa cadastrada no sistema.")
            else:
                for task in all_tasks:
                    print(task)

        elif choice == "4":
            try:
                task_id = int(
                    input("Digite o ID da tarefa a ser marcada como concluída: ")
                )
                if task_service.mark_task_as_completed(task_id):
                    print(f"Sucesso! Tarefa {task_id} marcada como concluída.")
                else:
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
            except ValueError:
                print("Erro: Por favor, digite um ID numérico válido.")

        elif choice == "5":
            try:
                task_id = int(input("Digite o ID da tarefa a ser removida: "))
                if task_service.delete_task(task_id):
                    print(f"Sucesso! Tarefa {task_id} foi removida.")
                else:
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
            except ValueError:
                print("Erro: Por favor, digite um ID numérico válido.")

        elif choice == "6":
            print("\n--- Visualizar Tarefa Única ---")
            try:
                task_id = int(input("Digite o ID da tarefa que deseja visualizar: "))
                task = task_service.get_task_by_id(task_id)

                if task:
                    print("Detalhes da Tarefa:")
                    print(task)
                else:
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
            except ValueError:
                print("Erro: Por favor, digite um ID numérico válido.")

        elif choice == "0":
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
