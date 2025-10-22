from datetime import datetime
from decimal import Decimal
from typing import Any
from pydantic import BaseModel, field_serializer


class CausacionIDs(BaseModel):
    id: int
class CausacionDTO(BaseModel):
    id_documento: int
    id_comprobante: int
    id_nit: int
    fecha: str
    fecha_manual: str
    id_cuenta: int
    valor: Any
    tipo: int
    concepto: str
    documento_referencia: str
    token: str | None
    extra: str
    
    model_config = {
        "from_attributes": True  # 👈 reemplaza orm_mode en v2
    }
    
class CausacionDTOEnding(BaseModel):
    id_documento: int
    id_comprobante: int
    id_nit: int
    nit: int
    fecha: str
    fecha_manual: str
    id_cuenta: int
    valor: str
    tipo: int
    concepto: str
    documento_referencia: str
    token: str | None
    extra: str
    
    model_config = {
        "from_attributes": True  # 👈 reemplaza orm_mode en v2
    }
    
 
# "fecha_manual":"2024-03-19",
# "valor":"100",
class CausacionDTOClose(BaseModel):
    id_documento: int
    id_comprobante: int
    id_nit: int
    fecha: datetime
    fecha_manual: datetime
    id_cuenta: int
    valor: float
    tipo: int
    concepto: str
    documento_referencia: str
    token: str | None
    extra: str
    
    model_config = {
        "from_attributes": True  
    }

      # 👇 Serializadores para JSON
    @field_serializer("fecha", "fecha_manual")
    def serialize_dt(self, v: datetime, _info):
        return v.isoformat()

    @field_serializer("valor")
    def serialize_decimal(self, v: Decimal, _info):
        return str(v)
    