from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Text

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    valor = Column(Float, default=10.0)
    metodo_pagamento = Column(String)  # 'pix', 'boleto', 'cartao'
    status = Column(String, default="pendente")
    data_criacao = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    acao = Column(String)  # Ex: "registro", "login_falhou"
    contexto = Column(Text)  # Ex: "email=teste@email.com"
    data = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="logs")

















    # wallet = relationship("Wallet", back_populates="owner", uselist=False)

# class Wallet(Base):
#     __tablename__ = "wallets"

#     id = Column(Integer, primary_key=True, index=True)
#     saldo = Column(Float, default=0.0)
#     user_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="wallet")
