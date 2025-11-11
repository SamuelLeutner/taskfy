from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Task(Base):
    """
    Representa uma tarefa com seus metadados (versão SQLAlchemy).
    Esta classe será mapeada para a tabela "task".

    Attributes:
        id_task (int): O identificador único da tarefa (Chave Primária).
        description (str): A descrição do que precisa ser feito.
        status (str): O estado atual da tarefa (ex: 'Pendente', 'Concluída').
        creation_date (datetime): A data e hora em que a tarefa foi criada.
        user_id_fk (int): Chave estrangeira para o usuário.
        category_id_fk (int): Chave estrangeira para a categoria.
    """

    __tablename__ = "task"
    id_task = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    status = Column(String(20), default="Pendente")
    creation_date = Column(TIMESTAMP, server_default=func.now())
    user_id_fk = Column(Integer, ForeignKey("user.id_user"), nullable=False)
    category_id_fk = Column(Integer, ForeignKey("category.id_category"), nullable=False)
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")

    def __str__(self):
        """Retorna uma representação amigável da tarefa em string."""

        data_formatada = (
            self.creation_date.strftime("%Y-%m-%d") if self.creation_date else "N/A"
        )

        return f"ID: {self.id_task} | Status: {self.status} | Descrição: {self.description}"
