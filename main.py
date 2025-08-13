#BACKEND
#main.py
from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
import uvicorn

# Configuração do middleware CORS
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todas as origens
        allow_credentials=True,  # Permite cookies/autorização entre domínios
        allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
        allow_headers=["*"],  # Permite todos os headers
        expose_headers=["*"]  # Expõe todos os headers na resposta
    )
]

# Configurar o aplicativo FastAPI com middlewares
app = FastAPI(
    title="AI Query Agent",
    description="Use natural language to query your database and download results.",
    middleware=middleware
)

# Middleware adicional para headers CORS (reforço)
@app.middleware("http")
async def add_cors_header(request, call_next):
    """
    Middleware adicional para garantir que os headers CORS estejam presentes em todas as respostas.
    """
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Incluir as rotas do roteador
app.include_router(router)

# Rota raiz para fornecer uma mensagem inicial
@app.get("/")
def read_root():
    return {
        "message": "Welcome to AI Query Agent! Use the /query endpoint to ask database queries in natural language."
    }

# Ponto de entrada para rodar o servidor
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
