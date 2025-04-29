from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import CausacionContable as CausacionContableModel
from app.shemas.shema_causacion_contable import CausacionContableCreate, CausacionContableUpdate, CausacionContable
from app.models import Configuration as ConfigurationModel

from app.config.config import decode_token, get_current_user 
from app.config.mail import AWS_BUCKET_NAME, AWS_S3_URL, s3_client
from datetime import datetime, timezone
import uuid

from dotenv import load_dotenv
load_dotenv() 
import os

version = os.getenv("API_VERSION")
router = APIRouter(prefix=f"/api/{version}", tags=['Causacion Contable'])

def dateNow(): 
    fecha_actual = datetime.now()
    return fecha_actual.strftime("%Y/%m/%d")

@router.post("/causacionContable", response_model=CausacionContable)
def create_causacion(causacion: CausacionContableCreate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    fecha_formateada = dateNow()
    db_causacion = CausacionContableModel(
        id_documento=None,
        id_comprobante=2,
        id_nit=causacion.id_nit,
        fecha=fecha_formateada,
        fecha_manual=causacion.fecha_manual,
        id_cuenta=6068094,
        valor=causacion.valor,
        tipo=1,
        concepto=causacion.concepto,
        documento_referencia=None,
        token=None,
        extra=None,
        user_id=tockendecode["sub"],
        estado="entregado",
    )
    db.add(db_causacion)
    db.commit()
    db.refresh(db_causacion)
    print(db_causacion.id)
    return db_causacion

@router.get("/causacionContable/{id}", response_model=CausacionContable)
def read_causacion(id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
    if db_causacion is None:
        raise HTTPException(status_code=404, detail="Causación no encontrada")
    return db_causacion

@router.get("/causacionContable", response_model=List[CausacionContable])
def read_causacion(db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    causaciones = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado != "entregado",
        CausacionContableModel.user_id == tockendecode["sub"]
    ).all()
    if not causaciones:
        raise HTTPException(status_code=404, detail="Causación no encontrada")
    return causaciones


def increment_counter(db):
    counter_config = db.query(ConfigurationModel).filter(ConfigurationModel.key == "counter").first()
    if not counter_config:
        raise HTTPException(status_code=404, detail="Configuración del contador no encontrada")
    try:
        current_value = int(counter_config.value)
        new_value = current_value + 1
        counter_config.value = str(new_value)
        counter_config.updated_at = datetime.now(timezone.utc)
        db.commit()
        return new_value, str(current_value)
    except ValueError:
        raise HTTPException(status_code=500, detail="El valor del contador no es un entero válido")
    
async def upload_file_helper(file: UploadFile):
    try:
        contents = await file.read()
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_id = str(uuid.uuid4())
        file_key = f"{unique_id}_{datetime.now().day}{datetime.now().month}.{file_extension}"
        s3_client.put_object(Bucket=AWS_BUCKET_NAME, Key=file_key, Body=contents)
        public_url = f"{AWS_S3_URL}/{AWS_BUCKET_NAME}/{file_key}"
        return  public_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")

 
@router.post("/activarCausacion")
async def read_causacion_and_update(db: Session = Depends(get_db), token: dict = Depends(get_current_user), file: UploadFile = File(...)):
    tockendecode = decode_token(token)
    causaciones = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == "entregado",
        CausacionContableModel.user_id == tockendecode["sub"]
    ).all()

    if not causaciones:
        raise HTTPException(status_code=404, detail="Causación no encontrada con estado 'entregado'")

    # Cambiamos el estado a "finalizado" y actualizamos los campos del documento
    _, codigo_documento = increment_counter(db)
    public_url = await upload_file_helper(file)

    for causacion in causaciones:
        causacion.estado = "activado"
        causacion.id_documento = str(codigo_documento)
        causacion.documento_referencia = public_url
        
    db.commit()
    
    return { "ms": "ok", "description": "Desea enviar más causaciones o desea cerrar las actividades de este mes" }
      

@router.post("/finalizarCausacion")
async def finalizarCausaciones(db: Session = Depends(get_db), token: dict = Depends(get_current_user), file: UploadFile = File(...)):
    tockendecode = decode_token(token)
    causaciones = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == "entregado",
        CausacionContableModel.user_id == tockendecode["sub"]
    ).all()

    if not causaciones:
        raise HTTPException(status_code=404, detail="Causación no encontrada con estado 'entregado'")

    for causacion in causaciones:
        causacion.estado = "finalizado"
        causacion.fecha = dateNow()
    db.commit()
    
    return { "ms": "ok", "description": f"Se han cerrado las causaciones del mes {dateNow().month}" }
      
      
        
@router.put("/causacionContable/{id}", response_model=CausacionContable)
def update_causacion(id: int, causacion: CausacionContableUpdate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
    if db_causacion is None:
        raise HTTPException(status_code=404, detail="Causación no encontrada")
    
    for key, value in causacion.__dict__(exclude_unset=True).items():
        setattr(db_causacion, key, value)
    
    db.commit()
    db.refresh(db_causacion)
    return db_causacion

@router.delete("/causacionContable/{id}", response_model=CausacionContable)
def delete_causacion(id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
    if db_causacion is None:
        raise HTTPException(status_code=404, detail="Causación no encontrada")
    
    db.delete(db_causacion)
    db.commit()
    return db_causacion