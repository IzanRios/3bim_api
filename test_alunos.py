from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import AlunoDB

client = TestClient(app)


def test_listar_alunos_com_mock():
    db_mock = MagicMock()
    # Retorna o modelo com a matricula em string, se seu Schema exigir string
    db_mock.query.return_value.all.return_value = [
        AlunoDB(id=1, nome='Lucas', matricula='12345', curso='infonet', email='lucas@gmail.com')
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    # CORREÇÃO 1: Rota ajustada de /produtos para /alunos
    resposta = client.get('/alunos')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'Lucas'

    app.dependency_overrides.clear()


def test_criar_aluno_com_mock():
    db_mock = MagicMock()

    # CORREÇÃO 2: Garante que a checagem de matrícula existente retorne None
    db_mock.query.return_value.filter.return_value.first.return_value = None

    def simular_refresh(aluno):
        aluno.id = 1  # Simula o banco atribuindo um ID ao registro

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    # CORREÇÃO 3: Removido o campo 'id' do payload
    novo_aluno = {
        'nome': 'Pedro',
        'matricula': '54321',
        'curso': 'administração',
        'email': 'pedro@gmail.com'
    }
    resposta = client.post('/alunos', json=novo_aluno)

    assert resposta.status_code == 201
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()