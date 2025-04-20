from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core_service.models import User

from core_service import models               # Importa os modelos do banco (User)
from core_service.database import SessionLocal  # Sessão do banco de dados
from . import schemas, utils                  # Importa os schemas (entrada/saída) e funções auxiliares (hash, token)

# Cria o grupo de rotas para autenticação
router = APIRouter()

# Função que fornece uma sessão do banco de dados para cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota POST /register – registra um novo usuário
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verifica se já existe um usuário com o mesmo e-mail
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Cria o hash da senha antes de salvar
    hashed_pw = utils.hash_password(user.password)

    # Cria um novo usuário com os dados recebidos e senha criptografada
    new_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)

    # Salva o usuário no banco
    db.add(new_user)
    db.flush()
    wallet = models.Wallet(user_id=new_user.id, saldo=0.0)
    db.add(wallet)

    db.commit()
    db.refresh(new_user)

    # Retorna os dados do novo usuário (sem senha)
    return new_user

# Rota POST /login – faz login e retorna o token JWT
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busca o usuário pelo username
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # Verifica se o usuário existe e se a senha está correta
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Gera o token JWT com o nome do usuário como "sub" (subject)
    access_token = utils.create_access_token(data={"sub": user.username})

    # Retorna o token de acesso
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")
    return user

@router.get("/wallet/me")
def get_my_wallet(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    if wallet is None:
        raise HTTPException(status_code=404, detail="Carteira não encontrada")
    return {"saldo": wallet.saldo}
