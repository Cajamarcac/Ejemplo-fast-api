from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

DATABASE_URL = "mysql+mysqlconnector://tu_nombre_de_usuario:tu_contraseña@localhost/tu_nombre_de_base_de_datos"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)

Base.metadata.create_all(bind=engine)

# Resto del código de tu aplicación FastAPI

app = FastAPI()

class User(BaseModel):
    username: str
    email: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

def fake_hash_password(password: str):
    return "fakehashed" + password

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def fake_decode_token(token):
    return TokenData(username=token + "decoded")

def get_current_user(token_data: TokenData = Depends(fake_decode_token)):
    return token_data

fake_users_db = {
    "user1": {
        "username": "user1",
        "email": "user1@example.com",
        "hashed_password": "fakehashedpassword1",
    },
    "user2": {
        "username": "user2",
        "email": "user2@example.com",
        "hashed_password": "fakehashedpassword2",
    },
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordBearer = Depends()):
    return {"access_token": form_data, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/users/{username}", response_model=User)
async def read_user(username: str):
    if username not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_users_db[username]
