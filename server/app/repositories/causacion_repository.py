import httpx
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import CausacionContable as CausacionContableModel
from app.shemas.shema_send_causacion import CausacionDTO, CausacionIDs
from datetime import datetime
from typing import List
from decimal import Decimal
from app.logs.logs import logger
from datetime import datetime
import json

class CausacionRepository:
    
    
    def ordenar_causacion_final(documentos): 
        fecha_manual = documentos["fecha_manual"]

        if isinstance(fecha_manual, datetime):
            fecha_manual = fecha_manual.strftime("%Y-%m-%d")
        elif isinstance(fecha_manual, str) and "T" in fecha_manual:
            fecha_manual = fecha_manual.split("T")[0]
        else:
            fecha_manual = str(fecha_manual)
        
        try:
            documentos_ordenados = {
                "id_documento": documentos["id_documento"],
                "id_comprobante": documentos["id_comprobante"],
                "id_nit": documentos["id_nit"],
                "fecha": documentos["fecha"],
                "fecha_manual": fecha_manual,
                "id_cuenta": documentos["id_cuenta"],
                "valor": Decimal(str(documentos["valor"])),
                "tipo": documentos["tipo"],
                "concepto": documentos["concepto"],
                "documento_referencia": documentos["documento_referencia"],
                "token": "",
                "extra": documentos["extra"]
            }
            print(documentos_ordenados)
            return documentos_ordenados
        except Exception as e:
            logger.error(f"Error al ordenar la causación: {str(e)}")
        return None
    
    def decimal_default(info):
        # convierte Decimal a float para que json.dumps acepte el objeto
        if isinstance(info, Decimal):
            return float(info)
        raise TypeError
    

    @classmethod
    async def enviar_causaciones_a_api(cls, documentos: List[CausacionDTO], causaciones, token: str, db: Session):
        url = f"http://begranda.com/equilibrium2/public/api/document?key={token}"
        payload_list = [cls.ordenar_causacion_final(c.model_dump()) for c in documentos]
        payload_serializado = json.dumps(payload_list, default=cls.decimal_default)
        logger.info(f"Payload a enviar Begranda: {payload_serializado}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data={"documents": payload_serializado},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                                
                causasids = [doc.model_dump() for doc in causaciones]
                mensaje = json.dumps({"documents": causasids}, ensure_ascii=False)
                logger.info(f"Datos Enviados Begranda: {mensaje}")
                            
                            
                for doct in causasids:
                    causacion = db.query(CausacionContableModel).filter(
                        CausacionContableModel.id == doct["id"],
                        CausacionContableModel.estado == "finalizado"
                    ).first()
                    
                    
                    if causacion:
                        report_str = json.dumps(response.json())
                        causacion.report_begranda = report_str  #[:250]  
                        causacion.begranda = datetime.now()
                    else: 
                        logger.error(f"Logger: Error al crear en begranda la causación contable de crédito: { report_str}")
                        db.commit()
                        return {
                            "status": "error",
                            "code": response.status_code,
                            "data": f"Logger: Error al crear en begranda la causación contable de crédito { report_str}"
                        }
                db.commit()
                return {
                    "status": "enviado",
                    "code": response.status_code,
                    "data": response.json()
                }
        except httpx.HTTPError as e:
            print(f"Error enviando causaciones: {str(e)}")
            logger.error(f"Except: Error al crear en begranda la causación contable de crédito: {str(e)}")
            return {
                "status": "error",
                "code": "http_error",
                "data": f"Except: Error al crear en begranda la causación contable de crédito {str(e)}" 
            }