from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base


class Compromisso(Base):
    __tablename__ = 'compromisso'

    id = Column("pk_compromisso", Integer, primary_key=True)
    nome = Column(String(300), unique=True)

    def __init__(self, nome: str):
        """
        Cria um Compromisso

        Arguments:
            nome: nome do produto.
        """
        self.nome = nome
