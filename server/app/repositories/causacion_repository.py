import httpx
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models import CausacionContable as CausacionContableModel
from app.shemas.shema_send_causacion import CausacionDTO, CausacionIDs
from datetime import datetime
from typing import List
from app.logs.logs import logger
import json

class CausacionRepository:

    @staticmethod
    async def enviar_causaciones_a_api(documentos: List[CausacionDTO], causaciones, token: str, db: Session):
        url = f"http://begranda.com/equilibrium2/public/api/document?key={token}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data={"documents": json.dumps([c.model_dump() for c in documentos])},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                
                causasids = [doc.model_dump() for doc in causaciones]
                for doct in causasids:
                    causacion = db.query(CausacionContableModel).filter(
                        CausacionContableModel.id == doct["id"],
                        CausacionContableModel.estado == "finalizado"
                    ).first()

                    if causacion:
                        report_str = json.dumps(response.json())
                        causacion.report_begranda = report_str[:250] 
                        causacion.begranda = datetime.now()
                    else: 
                        logger.error(f"Error al crear en begranda la causación contable de crédito: { report_str}")
                db.commit()
                 
                return {
                    "status": "enviado",
                    "code": response.status_code,
                    "data": response.json()
                }
        except httpx.HTTPError as e:
            print(f"Error enviando causaciones: {str(e)}")
            return {
                "status": "error",
                "detail": str(e)
            }
            
            
    