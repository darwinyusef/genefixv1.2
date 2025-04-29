# Genefix Conversion

1. Como observo las causaciones que se registraron
2. se puede editar algnos valores especificos manualmente? 

id_documento: comprobante de consecutivo -> ese id lo provee la empresa -> se debe comprobar con la empresa 
id_comprobante: https://begranda.com/equilibrium2/public/api/proof?key={{API_KEY}}
id_nit: http://begranda.com/equilibrium2/public/api/nits?key={{API_KEY}}&f-nit_1=123&eq-nit_1=123456789
fecha: envio
fecha_manual: documento ingreso de la causación -> no necesariamente son iguales pueden ser diferentes
id_cuenta: http://begranda.com/equilibrium2/public/api/account?eq-auxiliar=1&f-cuenta=13&key={{API_KEY}}&f-nombre=NACIONALES
valor: valor integer, max 2 decimales
tipo: debito (0) | credito (0)
concepto: text
documento_referencia: identificación sobre la factura que estoy cusando -> eso lo provee la empresa puede ir null -> revisar esta parte importante con la empresa 
tocken: debe haber una balanza entre credito y debito -> revisar con la empresa este codigo -> puede ir null | todas las transacciones por historico la manejan revisar con la empresa 
extra: texto abierto -> se podría revisar pero no hay implicaciones ya que no se imprime en el proceso
se evalua con la empresa como la gestión contable no se cruza entre credito y debito a nivel de documento para evitar problemas eso no pase 

eso depende del objetivo del desarrollo -> hay una serie de validaciones previas hay que revisar con contabilidad ese paso si hay que automatizar (debito/credito | hacer causacion en un mes cerrado cuando ya se pagaron impuestos)
