from sqlalchemy import Column, Integer, String, Float
from database import Base

# Modelo da tabela produtos
class ProdutoDB(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)


# Modelo da tabela alunos
class AlunoDB(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    matricula = Column(String(50), nullable=False, unique=True)
    curso = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)