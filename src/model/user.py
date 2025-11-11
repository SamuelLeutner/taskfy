from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base 


class User(Base):
    """
    Representa um Usuário no banco de dados.
    Esta classe será mapeada para a tabela "user".

    Attributes:
        id_user (int): O identificador único do usuário (Chave Primária).
        name (str): O nome do usuário.
        email (str): O email único do usuário.
    """

    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    tasks = relationship("Task", back_populates="user")
