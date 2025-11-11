from src.model.task import Task
from src.utils.db_session import get_db_session


class TaskService:
    """
    Gerencia a lógica de negócio para uma coleção de tarefas.
    Esta versão se conecta a um banco de dados PostgreSQL via SQLAlchemy.
    """

    def __init__(self):
        """Inicializa o serviço de tarefas."""
        pass

    def add_task(self, description: str, user_id: int, category_id: int) -> Task | None:
        """
        Cria e adiciona uma nova tarefa ao BANCO DE DADOS.

        Args:
            description (str): A descrição da tarefa.
            user_id (int): O ID do usuário associado.
            category_id (int): O ID da categoria associada.

        Returns:
            Task: O objeto da tarefa que foi criada, ou None se falhar.
        """
        db = get_db_session()
        try:
            new_task = Task(
                description=description,
                user_id_fk=user_id,
                category_id_fk=category_id,
            )
            db.add(new_task)
            db.commit()
            db.refresh(new_task)
            return new_task
        except Exception as e:
            db.rollback()
            print(f"Erro ao adicionar tarefa: {e}")
            return None
        finally:
            db.close()

    def list_all_tasks(self) -> list[Task]:
        """
        Retorna uma lista de TODAS as tarefas do banco de dados.

        Returns:
            list[Task]: Uma lista de objetos Task.
        """
        db = get_db_session()
        try:
            tasks = db.query(Task).all()
            return tasks
        finally:
            db.close()

    def list_pending_tasks(self) -> list[Task]:
        """
        Retorna uma lista de todas as tarefas com o status 'Pendente'.
        """
        db = get_db_session()
        try:

            tasks = db.query(Task).filter(Task.status == "Pendente").all()
            return tasks
        finally:
            db.close()

    def _find_task_by_id(self, db_session, task_id: int) -> Task | None:
        """
        Encontra uma tarefa na sessão do banco pelo seu ID.
        (Função auxiliar interna)
        """
        return db_session.query(Task).filter(Task.id_task == task_id).first()

    def get_task_by_id(self, task_id: int) -> Task | None:
        """
        Busca e retorna uma única tarefa pelo seu ID.

        Args:
            task_id (int): O ID da tarefa a ser encontrada.

        Returns:
            Task or None: O objeto da tarefa se encontrado, caso contrário None.
        """
        db = get_db_session()
        try:
            task = self._find_task_by_id(db, task_id)
            return task
        except Exception as e:
            print(f"Erro ao buscar tarefa: {e}")
            return None
        finally:
            db.close()

    def mark_task_as_completed(self, task_id: int) -> bool:
        """
        Altera o status de uma tarefa para 'Concluída' no banco.
        """
        db = get_db_session()
        try:
            task = self._find_task_by_id(db, task_id)

            if task:
                task.status = "Concluída"
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Erro ao marcar tarefa como concluída: {e}")
            return False
        finally:
            db.close()

    def delete_task(self, task_id: int) -> bool:
        """
        Remove uma tarefa do banco de dados.
        """
        db = get_db_session()
        try:
            task = self._find_task_by_id(db, task_id)

            if task:
                db.delete(task)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(f"Erro ao deletar tarefa: {e}")
            return False
        finally:
            db.close()
