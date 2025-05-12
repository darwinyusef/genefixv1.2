import json
import httpx
from typing import List
from app.shemas.shema_send_causacion import CausacionDTO

class CausacionRepository:

    @staticmethod
    async def enviar_causaciones_a_api(documentos: List[CausacionDTO], token: str):
        url = f"http://begranda.com/equilibrium2/public/api/document?key={token}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data={"documents": json.dumps([c.model_dump() for c in documentos])},
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
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
            
            
    