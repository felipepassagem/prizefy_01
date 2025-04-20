from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PagamentoCreate(BaseModel):
    metodo_pagamento: str
    valor: float = 10.0  # valor padrão

class PagamentoOut(BaseModel):
    id: int
    user_id: int
    metodo_pagamento: str
    valor: float
    status: str
    data_criacao: datetime

    class Config:
        orm_mode = True