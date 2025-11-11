from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base  


class Category(Base):
    """
    Representa uma Categoria para as tarefas.
    Esta classe será mapeada para a tabela "category".

    Attributes:
        id_category (int): O identificador único da categoria (Chave Primária).
        category_name (str): O nome da categoria (ex: "Trabalho").
    """

    __tablename__ = "category"

    id_category = Column(Integer, primary_key=True)
    category_name = Column(String(50), unique=True, nullable=False)

    tasks = relationship("Task", back_populates="category")
