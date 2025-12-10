import json
from typing import Optional
from xml.dom import ValidationErr
from pydantic import BaseModel

class ProceedingsDto(BaseModel):
    ciudad:Optional[str] = None

    nombre_remitente: Optional[str] = None
    
    tp_doc_remitente: Optional[str] = None
    identificacion_remitente: Optional[str] = None
    correo_remitente: Optional[str] = None
    telefono_remitente: Optional[str] = None
    direccion_remitente: Optional[str] = None
    tipo_de_producto: Optional[str] = None
    credito: Optional[str] = None


    asunto: Optional[str] = None
    mensaje: Optional[str] = None

    nombre_destinatario: Optional[str] = None
    correo_destinatario: Optional[str] = None
    identificacion_destinatario: Optional[str] = None

    nombre_del_destinatario: Optional[str] = None  # NOMBREDELDESTINATARIO
    dias_mora_historicos: Optional[str] = None      # DIASMORAHISTORICOS
    ruta_pdf: Optional[str] = None  
    user:Optional[str] = None  

    @classmethod
    def fromRaw(cls, rawBody: str):
        try:
            data = json.loads(rawBody)
            return cls(**data)
        except (json.JSONDecodeError, ValidationErr) as e:
            raise ValueError(f"Invalid scrapper request data: {e}")

