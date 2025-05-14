from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class CausacionContableBase(BaseModel):
    id_documento: Optional[int] = None
    id_comprobante: int
    id_nit: int
    nit: int
    fecha: datetime
    fecha_manual: date = None
    id_cuenta: int
    valor: float
    tipo: int
    concepto: str
    extra: str
    documento_referencia: Optional[str] = None
    token: Optional[str] = None

class CausacionContableCreate(CausacionContableBase):
    pass

class CausacionContableUpdate(BaseModel):
    id_nit: int
    nit: int
    fecha_manual: date = None
    valor: float
    concepto: str
    extra: str

class CausacionContable(CausacionContableBase):
    id: int
    estado: str
    ok: bool = True 
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
