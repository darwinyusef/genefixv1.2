from pydantic import BaseModel


class CausacionIDs(BaseModel):
    id: int
class CausacionDTO(BaseModel):
    id_documento: int
    id_comprobante: int
    id_nit: int
    fecha: str
    fecha_manual: str
    id_cuenta: int
    valor: str
    tipo: int
    concepto: str
    documento_referencia: str
    token: str | None
    extra: str