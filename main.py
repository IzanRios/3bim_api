from fastapi import FastAPI 
app = FastAPI()

@app.get('/')
def raiz():
    return {'mensagem': 'Minha primeira API em FastAPI!'}

@app.get('/clientes')
def clientes():
    return {'mensagem': 'Lista de Clientes!'}