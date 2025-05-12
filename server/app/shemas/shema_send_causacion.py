from pydantic import BaseModel

class CausacionDTO(BaseModel):
    id_documento: str
    id_comprobante: int
    id_nit: int
    fecha: str
    fecha_manual: str
    id_cuenta: int
    valor: str
    tipo: int
    concepto: str
    documento_referencia: str
    token: str
    extra: str