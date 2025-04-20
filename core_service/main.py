from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core_service.auth_service.routes import router as auth_router
from core_service.database import Base, engine

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração de CORS (libera acesso externo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque pelo domínio correto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota básica para teste
@app.get("/")
def read_root():
    return {"message": "API Prizefy online"}

# Importa as rotas de autenticação
app.include_router(auth_router, prefix="/auth")
