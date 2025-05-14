
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import custom_openapi
from app.controllers.auth_controller import router as auth_router
from app.controllers.user_controller import router as user_router
from app.controllers.causacion_contable_controller import router as causacion_router
from app.controllers.reset_password_controller import router as recover_pass
from app.config.mail import router as mail_router
from app.config.middleware_404 import  NotFoundMiddleware

from dotenv import load_dotenv
load_dotenv() 
import os

# Config JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Se define el esquema de seguridad

# Instancia de FastAPI
app = FastAPI()

# Gestar Configuracion OpenAPI
app.openapi = lambda: custom_openapi(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restringe esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=['Bienvenida'])
def material(): 
    return {
        "info": "bienvenido a genefix",
        "ms": "usted no tiene permisos para ingresar a esta plataforma"
        
    }
    

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(mail_router)
app.include_router(causacion_router)
app.include_router(recover_pass)

app.add_middleware(NotFoundMiddleware)
