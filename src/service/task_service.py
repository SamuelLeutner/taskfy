from model.task import Task


class TaskService:
    """
    Gerencia a lógica de negócio para uma coleção de tarefas.
    Esta classe não interage diretamente com o usuário (sem print ou input).
    """

    def __init__(self):
        """Inicializa o serviço de tarefas com uma lista vazia e um contador de ID."""
        self.tasks = []
        self._last_id = 0

    def add_task(self, description: str) -> Task:
        """
        Cria e adiciona uma nova tarefa à lista.

        Args:
            description (str): A descrição da tarefa a ser criada.

        Returns:
            Task: O objeto da tarefa que foi criada e adicionada.
        """
        self._last_id += 1
        new_task = Task(task_id=self._last_id, description=description)
        self.tasks.append(new_task)
        return new_task

    def list_pending_tasks(self) -> list:
        """
        Retorna uma lista de todas as tarefas com o status 'Pendente'.

        Returns:
            list: Uma lista de objetos Task que estão pendentes.
        """
        pending_tasks = []
        for task in self.tasks:
            if task.status == "Pendente":
                pending_tasks.append(task)
        return pending_tasks

    def _find_task_by_id(self, task_id: int) -> Task | None:
        """
        Encontra uma tarefa na lista pelo seu ID.

        Args:
            task_id (int): O ID da tarefa a ser encontrada.

        Returns:
            Task or None: O objeto da tarefa se encontrado, caso contrário None.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def mark_task_as_completed(self, task_id: int) -> bool:
        """
        Altera o status de uma tarefa para 'Concluída'.

        Args:
            task_id (int): O ID da tarefa a ser marcada como concluída.

        Returns:
            bool: True se a tarefa foi encontrada e marcada, False caso contrário.
        """
        task = self._find_task_by_id(task_id)
        if task:
            task.status = "Concluída"
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """
        Remove uma tarefa da lista.

        Args:
            task_id (int): O ID da tarefa a ser removida.

        Returns:
            bool: True se a tarefa foi encontrada e removida, False caso contrário.
        """
        task = self._find_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def list_all_tasks(self) -> list:
        """
        Retorna uma lista de todas as tarefas, independentemente do status.

        Returns:
            list: Uma lista de todos os objetos Task.
        """
        return self.tasks
