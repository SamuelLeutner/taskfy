import datetime

class Task:
    """
    Representa uma tarefa com seus metadados.

    Attributes:
        task_id (int): O identificador único da tarefa.
        description (str): A descrição do que precisa ser feito.
        creation_date (datetime): A data e hora em que a tarefa foi criada.
        status (str): O estado atual da tarefa (ex: 'Pendente', 'Concluída').
    """

    def __init__(self, task_id, description):
        """
        Inicializa uma nova tarefa.

        Args:
            task_id (int): O ID para a nova tarefa.
            description (str): A descrição da nova tarefa.
        """
        self.task_id = task_id
        self.description = description
        self.creation_date = datetime.datetime.now()
        self.status = "Pendente"

    def __str__(self):
        """Retorna uma representação amigável da tarefa em string."""
        return f"ID: {self.task_id} | Status: {self.status} | Descrição: {self.description}"
