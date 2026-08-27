from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB, AlunoDB
from schemas import (
    ProdutoCreate,
    ProdutoResponse,
    AlunoCreate,
    AlunoResponse
)
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
def criar_tabelas():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # em produção, restringir para o domínio real do front-end
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()

# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db:
Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
        
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)
    return produto

@app.get("/alunos", response_model=list[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(AlunoDB).all()

@app.post("/alunos", response_model=AlunoResponse, status_code=201)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    aluno_existente = db.query(AlunoDB).filter(
        AlunoDB.matricula == aluno.matricula
        ).first()
    if aluno_existente:
        raise HTTPException(
            status_code=400,
            detail="Matrícula já cadastrada"
        )
    novo_aluno = AlunoDB(**aluno.model_dump())
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

@app.get("/alunos/{aluno_id}", response_model=AlunoResponse)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoDB).filter(AlunoDB.id == aluno_id).first()
    if aluno is None:
        raise HTTPException(status_code=404, detail='Aluno não encontrado')
    return aluno

@app.delete("/alunos/{aluno_id}", status_code=204)
def remover_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    aluno = db.query(AlunoDB).filter(
        AlunoDB.id == aluno_id
    ).first()
    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )
    db.delete(aluno)
    db.commit()

@app.put("/alunos/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoCreate,
    db: Session = Depends(get_db)
):
    aluno = db.query(AlunoDB).filter(
        AlunoDB.id == aluno_id
    ).first()
    if aluno is None:
        raise HTTPException(
            status_code=404,
            detail="Aluno não encontrado"
        )
    aluno.nome = dados.nome
    aluno.matricula = dados.matricula
    aluno.curso = dados.curso
    aluno.email = dados.email
    db.commit()
    db.refresh(aluno)
    return aluno