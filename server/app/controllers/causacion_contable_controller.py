from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.config.database import get_db
from app.models import CausacionContable as CausacionContableModel
from app.shemas.shema_causacion_contable import CausacionContableCreate, CausacionContableUpdate, CausacionContable, FinCausacionModel
from app.models import Configuration as ConfigurationModel
from app.shemas.shema_send_causacion import CausacionDTO, CausacionIDs, CausacionDTOEnding, CausacionDTOClose
from app.repositories.causacion_repository import CausacionRepository

from app.config.config import decode_token, get_current_user 
from app.config.upload_files import upload_file_helper
from datetime import datetime, timezone
from app.logs.logs import logger
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
@router.post("/finalizarCausacion")
async def read_causacion_and_update(data: FinCausacionModel, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    try:
        tockendecode = decode_token(token)
        causaciones = db.query(CausacionContableModel).filter(
            CausacionContableModel.estado == "activado",
            CausacionContableModel.user_id == tockendecode["sub"]
        ).all()
        if not causaciones: 
            return {
                "status_code": status.HTTP_204_NO_CONTENT,
                "message": "No se encontraron causaciones activas para este usuario",
                "content": 0
            }

        documentos = []
        idCausaciones = []
        idcuenta = int(data.id_cuenta)
        nuevo = await credito_causacion_contable(idcuenta, causaciones, db, token)
        if not nuevo:   
            logger.error("Error al crear la causación de crédito", extra={"causaciones": causaciones})
            raise HTTPException(status_code=500, detail="Error al crear la causación de crédito")
        
        
       
        for causacion in causaciones:
            causacion.estado = "finalizado"
            causacion.id_cuenta = idcuenta
            idCausaciones.append(CausacionIDs(id=causacion.id))
            documentos.append(CausacionDTO(
                id_documento=causacion.id_documento,
                id_comprobante=causacion.id_comprobante,
                id_nit=causacion.id_nit,
                fecha=str(causacion.fecha),
                fecha_manual=str(causacion.fecha_manual),
                id_cuenta=idcuenta,
                valor=str(causacion.valor),
                tipo=1,
                concepto=causacion.concepto,
                documento_referencia=str(causacion.documento_referencia),
                token="",
                extra=str(causacion.extra)
            ))
        
        documentos.append(nuevo)
        idCausaciones.append(CausacionIDs(id=nuevo.id_documento))
        #print(len(documentos), len(idCausaciones))
        
        db.commit()
        # Enviamos a API externa
        resultado_envio = await CausacionRepository.enviar_causaciones_a_api(documentos, idCausaciones, token=tokenbegranda, db=db)
        if not resultado_envio:
            logger.error("Error al enviar las causaciones a la API externa", extra={"documentos": documentos, "idCausaciones": idCausaciones})
            raise HTTPException(status_code=500, detail="Error al enviar las causaciones a la API externa")
        
        # print(resultado_envio)
        
        return { "ms": "ok", "description": "Desea enviar más causaciones o desea cerrar las actividades de este mes", "res_begranda": resultado_envio, "credito": "true" }
    except Exception as e:
        logger.error(f"Error al finalizar la causación contable: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al finalizar la causación contable: {str(e)}")


async def credito_causacion_contable(
    id_cuenta: int,
    documentos: List[CausacionDTOEnding], 
    db: Session = Depends(get_db), 
    token: dict = Depends(get_current_user)
):
    try:
        tockendecode = decode_token(token)
        fecha_formateada = dateNow()
        
        if documentos: 
            total_valor = sum(float(d.valor) for d in documentos)    
            base = documentos[0]

            nuevo = CausacionContableModel(
                id_documento=base.id_documento,   
                id_comprobante=18,
                id_nit=248,
                nit=base.nit,
                fecha=fecha_formateada.isoformat() if isinstance(fecha_formateada, datetime) else str(fecha_formateada),
                fecha_manual=base.fecha_manual.isoformat() if isinstance(base.fecha_manual, datetime) else str(base.fecha_manual),
                id_cuenta=id_cuenta,
                valor=total_valor,
                tipo=1,
                concepto="LEGALIZACIÓN DE CAJA MENOR",
                documento_referencia=str(base.documento_referencia),
                token=base.token,
                extra=base.extra,
                user_id=tockendecode["sub"],
                estado="finalizado",
            )
            db.add(nuevo)
            db.commit()
            db.refresh(nuevo)

        return CausacionDTOClose.model_validate(nuevo)
    
    except Exception as e:
        logger.error(f"Error al crear la causación contable de crédito: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al crear la causación contable de crédito: {str(e)}")


# 🤓 ♦♣♠
@router.post("/activarCausacion")
async def read_causacion_and_update(db: Session = Depends(get_db), token: dict = Depends(get_current_user), file: UploadFile = File(...)):
    try:
        tockendecode = decode_token(token)
        causaciones = db.query(CausacionContableModel).filter(
            CausacionContableModel.estado == "entregado",
            CausacionContableModel.user_id == tockendecode["sub"]
        ).all()
        if causaciones == 0:
            return { "status_code": status.HTTP_204_NO_CONTENT, "content": 0 }

        # Cambiamos el estado a "finalizado" y actualizamos los campos del documento
        _, codigo_documento = increment_counter(db)
        public_url = await upload_file_helper(file)

        for causacion in causaciones:
            causacion.estado = "activado"
            causacion.id_documento = str(codigo_documento)
            causacion.documento_referencia = public_url

        db.commit()
        return { "ms": "ok", "description": "Desea enviar más causaciones o desea cerrar las actividades de este mes" }
    except Exception as e:
        logger.error(f"Error en /activarCausacion: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error en /activarCausacion: {str(e)}")
    
    
# 🤓 ♦♣♠    
@router.put("/causacionContable/{id}", response_model=CausacionContable)
def update_causacion(id: int, causacion: CausacionContableUpdate, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    try:
        db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
        if db_causacion is None:
            raise HTTPException(status_code=404, detail="Causación no encontrada")

        for key, value in causacion.dict(exclude_unset=True).items():
            setattr(db_causacion, key, value)

        db.commit()
        db.refresh(db_causacion)
        return db_causacion
    except Exception as e:
        logger.error(f"Error al actualizar causación con id {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al actualizar causación: {str(e)}")


@router.delete("/causacionContable/{id}", response_model=CausacionContable)
def delete_causacion(id: int, db: Session = Depends(get_db), token: dict = Depends(get_current_user)):
    try:
        db_causacion = db.query(CausacionContableModel).filter(CausacionContableModel.id == id).first()
        if db_causacion is None:
            raise HTTPException(status_code=404, detail="Causación no encontrada")

        db.delete(db_causacion)
        db.commit()
        return db_causacion
    except Exception as e:
        logger.error(f"Error al eliminar causación con id {id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error al eliminar causación: {str(e)}")
