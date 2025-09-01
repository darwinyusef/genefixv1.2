from fastapi import HTTPException, status, Depends, Response
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from app.shemas.shema_auth import LoginRequest, TokenResponse
from app.config.config import get_current_user, generate_csrf_token, hash_password, verify_password
from app.config.database import get_db
from app.models import User
from sqlalchemy.orm import Session
from app.logs.logs import logger
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv() 
import os

version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}")

# Config JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Crear token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=3))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def get_all_token_data(token: TokenResponse) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire_timestamp = payload.get("exp")
        if expire_timestamp is not None:
            expire_datetime = datetime.fromtimestamp(expire_timestamp, tz=timezone.utc)
            if expire_datetime < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token expirado")
        else:
            raise HTTPException(status_code=400, detail="Token sin fecha de expiración")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    return payload

# Ruta de login usando JSON response_model=TokenResponse,
@router.post("/logina", tags=["Auth"],  status_code=status.HTTP_200_OK)
async def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == login_data.username).first()
        
    if verify_password(login_data.password, db_user.password) == False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if login_data.username != db_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
        
    if db_user.rol == "inactive":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )

    csrf_token = get_csrf_token(login_data, db_user, db)
    
    login_data = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "username": db_user.username,
        "rol": db_user.rol,
        "password": None,
        "approval_token": csrf_token,
        "api": os.getenv("API_VERSION")
    }
    
    if "password" in login_data:
        del login_data["password"]
 
    response.set_cookie("csrf_token", csrf_token, httponly=True, samesite="Lax")
          
    payload = {
        "sub": str(login_data["id"]),   
        "user_data": login_data, 
    }
    
    token = create_access_token(payload)
    
    return JSONResponse(
        content={
        "ms": "active_csrf_token",
        "access_token": token, 
        "token_type": "bearer",
        "user": login_data
    })


@router.post("/login", tags=["Auth"], status_code=status.HTTP_200_OK)
async def login(login_data: LoginRequest, response: Response, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == login_data.username).first()
   
    if not db_user or not verify_password(login_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    if db_user.rol == "inactive":
        logger.error("HTTP_401_UNAUTHORIZED", extra={"ms": "HTTP_401_UNAUTHORIZED", "detail": login_data})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )

    csrf_token = get_csrf_token(login_data, db_user, db)

    user_info = {
        "id": db_user.id,
        "name": db_user.name,
        "email": db_user.email,
        "username": db_user.username,
        "rol": db_user.rol,
        "approval_token": csrf_token,
        "api": os.getenv("API_VERSION")
    }

    response.set_cookie("csrf_token", csrf_token, httponly=True, samesite="Lax")

    payload = {
        "sub": str(db_user.id),
        "user_data": user_info,
    }

    token = create_access_token(payload)

    return JSONResponse(
        content={
            "ms": "active_csrf_token",
            "access_token": token,
            "token_type": "bearer",
            "user": user_info
        }
    )




    
# firma administrativa para obtener permisos de movimientos 
def get_csrf_token(login_data, db_user: User, db):
    # print(login_data)
    try:
        if db_user.rol == "admin":
            # Generar el CSRF token
            csrf_token = generate_csrf_token()
            # Guardar el token de aprobación en el usuario
            db_user.approval_token = csrf_token
            # Agregar el usuario al DB y hacer commit
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            # Si todo sale bien, puedes devolver algo o continuar normalmente
            return csrf_token

    except Exception as e:
        # Capturamos cualquier excepción y la mostramos en los logs
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al procesar la solicitud: {str(e)}")



# Ruta protegida
@router.get("/profile", tags=["Profile"])
async def get_me(token: dict = Depends(get_current_user)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token requerido en Authorization header")
    try:
        payload = get_all_token_data(token)
        return JSONResponse({"mensaje": "¡Estás autenticado!", "token": payload})
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
