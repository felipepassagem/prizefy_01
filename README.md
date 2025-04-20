# 🏆 Prizefy – Backend

API desenvolvida em FastAPI para o projeto Prizefy, um sistema local de sorteios com carteira de usuário.

## 🚀 Funcionalidades atuais

- Registro de usuários
- Login com autenticação JWT
- Criação automática de carteira com saldo inicial
- Consulta de saldo do usuário autenticado

## 🔧 Tecnologias

- Python 3.10+
- FastAPI
- SQLite (desenvolvimento)
- SQLAlchemy
- JWT (`python-jose`)
- Bcrypt (`passlib`)
- `dotenv` para variáveis de ambiente

## ⚙️ Como rodar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/prizefy_01.git
cd prizefy_01

python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt

SECRET_KEY=sua_chave_muito_secreta

set PYTHONPATH=.
uvicorn core_service.main:app --reload

6. Acesse a documentação interativa
http://localhost:8000/docs

