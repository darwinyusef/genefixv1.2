from typing import List

from fastapi import APIRouter
from fastapi import HTTPException, Depends
from app.shemas.shema_user import UserCreate, UserUpdate, UserRolActive, UserOut
from fastapi.responses import JSONResponse
from app.config.config import decode_token, generate_csrf_token, hash_password
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from datetime import datetime, timezone
from app.config.config import get_current_user
from dotenv import load_dotenv
load_dotenv() 
import os

version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}")

# Crear usuario
@router.post("/register", tags=["Auth"], response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Document already registered")
    new_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        rol="inactive",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.model_validate(new_user)

# Crear usuario
@router.put("/activate", tags=["Users"], response_model=UserOut)
def activate_user(user: UserRolActive, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    if tockendecode['user_data']["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    act_user = db.query(User).filter(User.username == user.username).first()
    if not act_user:
        raise HTTPException(status_code=404, detail="User not found")

    act_user.rol = user.rol
    act_user.name = user.name
    
    db.commit()
    db.refresh(act_user)
    return UserOut.model_validate(act_user)



# Editar usuario
@router.put("/users/{user_id}", tags=["Users"], response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    db_user = db.query(User).filter(User.id == tockendecode['sub']).first()
    if tockendecode['user_data']["rol"] != "admin":
        db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_user)
    return db_user

# Listar usuarios
@router.get("/users", tags=["Users"], response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    if tockendecode['user_data']["rol"] != "admin":
        raise HTTPException(status_code=403, detail="Permission denied")
    
    users = db.query(User).all()
    return users

# Obtener usuario por ID
# TODO 🤓 hay que revisar porque no filtra para admin
@router.get("/users/{id}", tags=["Users"], response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    if tockendecode['user_data']["rol"] != "admin":
        user = db.query(User).filter(User.id == id).first()
    else:     
        user = db.query(User).filter(User.id == tockendecode['sub']).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
