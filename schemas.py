from pydantic import BaseModel


class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# ALUNO
# =========================

class AlunoCreate(BaseModel):
    nome: str
    matricula: str
    curso: str
    email: str


class AlunoResponse(BaseModel):
    id: int
    nome: str
    matricula: str
    curso: str
    email: str

    class Config:
        from_attributes = True