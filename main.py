from utils.menu import print_menu
from service.task_service import TaskService

def main():
    """
    Função principal que executa o loop do menu interativo.
    Esta função é responsável por toda a interação com o usuário.
    """
    task_service = TaskService()

    while True:
        print_menu()
        choice = input("Escolha uma opção: ")

        if choice == "1":
            description = input("Digite a descrição da nova tarefa: ")
            added_task = task_service.add_task(description)
            print(
                f"\nSucesso! Tarefa '{added_task.description}' (ID: {added_task.task_id}) foi adicionada."
            )

        elif choice == "2":
            pending_tasks = task_service.list_pending_tasks()
            print("\n--- Tarefas Pendentes ---")
            if not pending_tasks:
                print("Nenhuma tarefa pendente no momento.")
            else:
                for task in pending_tasks:
                    print(task)

        
        elif choice == "3":
            
            all_tasks = task_service.list_all_tasks()

            
            print("\n--- Todas as Tarefas (Pendentes e Concluídas) ---")
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
                success = task_service.mark_task_as_completed(task_id)
                if success:
                    print(
                        f"Sucesso! Tarefa com ID {task_id} foi marcada como concluída."
                    )
                else:
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
            except ValueError:
                print("Erro: Por favor, digite um número de ID válido.")

        elif choice == "5":  
            try:
                task_id = int(input("Digite o ID da tarefa a ser removida: "))
                success = task_service.delete_task(task_id)
                if success:
                    print(f"Sucesso! Tarefa com ID {task_id} foi removida.")
                else:
                    print(f"Erro: Tarefa com ID {task_id} não encontrada.")
            except ValueError:
                print("Erro: Por favor, digite um número de ID válido.")

        elif choice == "6":  
            print("Saindo do programa. Até mais!")
            break

        else:
            print("Opção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
