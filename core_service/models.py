from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    wallet = relationship("Wallet", back_populates="owner", uselist=False)

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    saldo = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="wallet")
