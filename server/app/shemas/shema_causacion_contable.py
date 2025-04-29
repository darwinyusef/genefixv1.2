from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class CausacionContableBase(BaseModel):
    id_documento: Optional[str] = None
    id_comprobante: int
    id_nit: int
    fecha: datetime
    fecha_manual: date = None
    id_cuenta: int
    valor: float
    tipo: int
    concepto: str
    documento_referencia: Optional[str] = None
    token: Optional[str] = None
    extra: Optional[str] = None

class CausacionContableCreate(CausacionContableBase):
    pass

class CausacionContableUpdate(CausacionContableBase):
    pass

class CausacionContable(CausacionContableBase):
    id: int
    estado: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
