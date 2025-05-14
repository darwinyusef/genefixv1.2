from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.config.config import hash_password
from app.config.database import get_db
from app.shemas.shema_configuration import RecoverPassRequest, ChangeRequest
from app.models import Configuration, User

from dotenv import load_dotenv
load_dotenv() 
import os

version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}", tags=['Auth'])

@router.get("/solicitude")
def solicitude(db: Session = Depends(get_db)):
    config = (
        db.query(Configuration)
        .options(joinedload(Configuration.user)) 
        .filter(Configuration.key == 'recover_pass')
        .all()
    )
    
    return {"ms": "ok", "config": config}

@router.post("/recover-pass")
def recover_pass(request: RecoverPassRequest, db: Session = Depends(get_db)):
    # 1. Buscar el usuario por email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Verificar si ya existe una solicitud activa
    existing = db.query(Configuration).filter(
        Configuration.key == "recover_pass",
        Configuration.state == "active",
        Configuration.value == "solicitude",
        Configuration.type == request.type,
        Configuration.id_user == user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una solicitud activa de recuperación")

    # 3. Crear nueva solicitud
    new_conf = Configuration(
        key="recover_pass",
        value="solicitude",
        description="El usuario solicita recuperación de password",
        type=request.type,
        state="active",
        id_user=user.id
    )
    db.add(new_conf)
    db.commit()
    db.refresh(new_conf)

    return {"message": "ok", "id": new_conf.id}


@router.put("/recover-pass/{id}")
def update_recover_pass(id: int, request: ChangeRequest, db: Session = Depends(get_db)):
    config = db.query(Configuration).filter(Configuration.id == id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    if config.value == "solicitude":
        user = db.query(User).filter(User.id == config.id_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if config.type == "email":
            user.email = request.change
        elif config.type == "password":
            user.password = hash_password(request.change)
        
        db.add(user) 
        config.state = "completed"
        config.value = "close"
        db.add(config) 

        db.commit()
        return {"message": f"Estado actualizado a completed"}
    else: 
        return {"message": f"No tiene solicitudes activas"}
    

    