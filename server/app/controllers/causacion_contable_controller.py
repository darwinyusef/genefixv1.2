from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.config.database import get_db
from app.models import CausacionContable as CausacionContableModel
from app.shemas.shema_causacion_contable import CausacionContableCreate, CausacionContableUpdate, CausacionContable
from app.models import Configuration as ConfigurationModel
from app.shemas.shema_send_causacion import CausacionDTO, CausacionIDs
from app.repositories.causacion_repository import CausacionRepository

from app.config.config import decode_token, get_current_user 
from app.config.mail import AWS_BUCKET_NAME, AWS_S3_URL, s3_client
from datetime import datetime, timezone
import uuid

from dotenv import load_dotenv

load_dotenv() 
import os

version = os.getenv("API_VERSION")
tokenbegranda = os.getenv("TOKEN_BEGRANDA")
router = APIRouter(prefix=f"/api/{version}", tags=['Causacion Contable'])

def dateNow(): 
    fecha_actual = datetime.now()
    return fecha_actual.strftime("%Y/%m/%d")

# 🤓 ♦♣♠
def convertir_mes_a_numero(nombre_mes: str) -> int:
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    return meses.get(nombre_mes.lower(), 0)
                     
                     
# 🤓 ♦♣♠
@router.get("/causacionContable")
def read_causacion(type: str = Query("entregado"), db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    causaciones = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == type,
        CausacionContableModel.user_id == tockendecode["sub"]
    ).all()
    
    causacionescount = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == type,
        CausacionContableModel.user_id == tockendecode["sub"]
    ).count()
    
    if causacionescount == 0:
        return { "status_code": status.HTTP_204_NO_CONTENT, "content":0 }
    return causaciones


# 🤓 ♦♣♠
@router.get("/causacionesFinalContables")
def read_causacion(
    type: str = Query("finalizado"),  
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1), 
    nit: Optional[int] = Query(None),
    anio: Optional[str] = Query(None),
    mes: Optional[str] = Query(None),
    db: Session = Depends(get_db), 
    token: dict = Depends(get_current_user)
    ):
    tockendecode = decode_token(token)
    query = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == type,
        CausacionContableModel.user_id == tockendecode["sub"]
    )
    
    if anio and mes:
        query = query.filter(
                        extract('year', CausacionContableModel.fecha) == int(anio),
                        extract('month', CausacionContableModel.fecha) == int(convertir_mes_a_numero(mes))
                        )
    
    if nit: 
        query = query.filter(
                        CausacionContableModel.nit == nit
                        )
        
    total = query.count()
    resultados = query.offset(skip).limit(limit).all()
    
    if total == 0:
        return { "status_code": status.HTTP_204_NO_CONTENT, "content":0 }
    return {
        "total": total,
        "data": resultados,
        "skip": skip,
        "limit": limit
    }
    
# 🤓 ♦♣♠
@router.post("/causacionContable", response_model=CausacionContable)
def create_causacion(causacion: CausacionContableCreate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    fecha_formateada = dateNow()
    db_causacion = CausacionContableModel(
        id_documento=None,
        id_comprobante=2,
        id_nit=causacion.id_nit,
        nit=causacion.nit,
        fecha=fecha_formateada,
        fecha_manual=causacion.fecha_manual,
        id_cuenta=causacion.id_cuenta,
        valor=causacion.valor,
        tipo=1,
        concepto=causacion.concepto,
        documento_referencia=None,
        token=None,
        extra=causacion.extra,
        user_id=tockendecode["sub"],
        estado="entregado",
    )
    db.add(db_causacion)
    db.commit()
    db.refresh(db_causacion)
    # print(db_causacion.id)
    return db_causacion

# 🤓 ♦♣♠
@router.get("/causacionContable/{id}", response_model=CausacionContable)
def read_causacion(id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
    if db_causacion is None:
        raise HTTPException(status_code=404, detail="Causación no encontrada")
    return db_causacion

# 🤓 ♦♣♠
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
   
# 🤓 ♦♣♠ 
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

# 🤓 ♦♣♠
@router.post("/finalizarCausacion")
async def read_causacion_and_update(db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    tockendecode = decode_token(token)
    causaciones = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == "activado",
        CausacionContableModel.user_id == tockendecode["sub"]
    ).all()
    if causaciones == 0:
        return { "status_code": status.HTTP_204_NO_CONTENT, "content":0 }

    documentos = []
    idCausaciones = []
    for causacion in causaciones:
        causacion.estado = "finalizado" 
        idCausaciones.append(CausacionIDs(id=causacion.id))
        documentos.append(CausacionDTO(
            id_documento=causacion.id_documento,
            id_comprobante=causacion.id_comprobante,
            id_nit=causacion.id_nit,
            fecha=str(causacion.fecha),
            fecha_manual=str(causacion.fecha_manual),
            id_cuenta=causacion.id_cuenta,
            valor=str(causacion.valor),
            tipo=causacion.tipo,
            concepto=causacion.concepto,
            documento_referencia=str(causacion.documento_referencia),
            token="",
            extra=str(causacion.extra)
        ))
    
    db.commit()
    # Enviamos a API externa
    resultado_envio = await CausacionRepository.enviar_causaciones_a_api(documentos, idCausaciones, token=tokenbegranda, db=db)
    
    return { "ms": "ok", "description": "Desea enviar más causaciones o desea cerrar las actividades de este mes", "res_begranda": resultado_envio }
      

# 🤓 ♦♣♠
@router.post("/activarCausacion")
async def read_causacion_and_update(db: Session = Depends(get_db), token: dict = Depends(get_current_user), file: UploadFile = File(...)):
    tockendecode = decode_token(token)
    causaciones = db.query(CausacionContableModel).filter(
        CausacionContableModel.estado == "entregado",
        CausacionContableModel.user_id == tockendecode["sub"]
    ).all()
    if causaciones == 0:
        return { "status_code": status.HTTP_204_NO_CONTENT, "content":0 }

    # Cambiamos el estado a "finalizado" y actualizamos los campos del documento
    _, codigo_documento = increment_counter(db)
    public_url = await upload_file_helper(file)

    for causacion in causaciones:
        causacion.estado = "activado"
        causacion.id_documento = str(codigo_documento)
        causacion.documento_referencia = public_url
        
    db.commit()
    # print(causaciones)
    return { "ms": "ok", "description": "Desea enviar más causaciones o desea cerrar las actividades de este mes" }
      
# 🤓 ♦♣♠    
@router.put("/causacionContable/{id}", response_model=CausacionContable)
def update_causacion(id: int, causacion: CausacionContableUpdate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
    if db_causacion is None:
        raise HTTPException(status_code=404, detail="Causación no encontrada")
    
    for key, value in causacion.dict(exclude_unset=True).items():
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