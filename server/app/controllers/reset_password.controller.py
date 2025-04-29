from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException, Depends
import secrets

from app.config.database import get_db
from datetime import datetime, timezone
from app.models import PasswordResetToken, User  # tus modelos

from dotenv import load_dotenv
load_dotenv() 
import os

version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}")

@router.post("/password/forgot", tags=["Auth"])
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Crear token seguro
    token = secrets.token_urlsafe(32)

    # Guardar o actualizar el token en la tabla
    reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.email == email).first()

    if reset_token:
        reset_token.token = token
        reset_token.created_at = datetime.now(timezone.utc)
    else:
        reset_token = PasswordResetToken(
            email=email,
            token=token,
            created_at=datetime.now(timezone.utc)
        )
        db.add(reset_token)

    db.commit()

    # Aquí normalmente enviarías un email con el token
    return {"message": "Token de reseteo generado", "token": token}