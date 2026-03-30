from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def hello_world():
    return "HELLO WORLD!"

@app.get("/log")
def print_log(username, esito):
    return {
    'username': username,
    'esito':esito
    }
    
@app.post("/log")
def post_log(username, esito):
    print( {
    'username': username,
    'esito':esito
    })

@app.get("/saluta")
def saluta(nome: str):
    return {"messaggio": f"Ciao, {nome}!"}

@app.get("/greet")
def greet(name: str = "Mondo"):
    return {"message": f"Ciao, {name}!"}

@app.get("/sum")
def sum_numbers(a: int, b: int):
    return {"result": a + b}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

# http://127.0.0.1:8000/saluta?nome=Marco