import pandas as pd
import logging
from app.domain.interfaces.IGetProceedingsService import IGetProceedingsService
from app.application.dto.ProceedingsDto import ProceedingsDto
import json

from app.domain.interfaces.IDataBase import IDataBase
from app.infrastucture.database.repositories.DocumentRepository import DocumentRepository


class GetProceedingsService(IGetProceedingsService):

    

    def __init__(self, repository: DocumentRepository):
        self.repository= repository
        self.logger = logging.getLogger(__name__)
        
    async def get_proceedings(self,conn):
        try:
            excel_path = "/app/output/base/Base Notificaciones Compra.xlsx"
            df = pd.read_excel(excel_path)

            # Normalizar encabezados
            df.columns = df.columns.str.strip().str.upper()

            proceedings_list = []
            user_counter = 1  
            for _, row in df.iterrows():
                ident_raw = self._clean(row.get("IDENTIFICACION_REMITENTE"))

                if ident_raw:
                    ident_sin_guion = ident_raw.split("-")[0].strip()
                else:
                    ident_sin_guion = ""

                mensaje_raw = self._clean(row.get("MENSAJE"))
                nombre_dest = self._clean(row.get("NOMBREDELDESTINATARIO"))

                credito=self._clean(row.get("CREDITO"))

                # Reemplazar marcador por el nombre real del destinatario
                    # Procesar mensaje dinámicamente desde el Excel
                if mensaje_raw:
                    # 1. Reemplazar marcador "(Nombre destinatario)"
                    mensaje_final = mensaje_raw.replace("(Nombre destinatario)", nombre_dest)

                    # 2. Convertir saltos de Excel (\r\n o \n) a saltos de párrafo dobles
                    mensaje_final = (
                        mensaje_final
                        .replace("\r\n", "\n")
                        .replace("\n", "\n\n")  # Cada salto → doble salto para párrafos
                        .strip()
                    )
                else:
                    mensaje_final = ""


            
                if user_counter > 10:
                    user_counter = 1

                dto = ProceedingsDto(
                    ciudad="BOGOTA",

                    # REMITENTE
                    nombre_remitente=self._clean(row.get("NOMBRE_REMITENTE")),
                    tp_doc_remitente=self._clean(row.get("TP_DOC_REMITENTE")),
                    identificacion_remitente = ident_sin_guion,
                    correo_remitente=self._clean(row.get("CORREO_REMITENTE")),
                    telefono_remitente=self._clean(row.get("TELEFONO_REMITENTE")),
                    direccion_remitente=self._clean(row.get("DIRECCION_REMITENTE")),
                    tipo_de_producto=self._clean(row.get("TIPODEPRODUCTO")),
                    credito=self._clean(row.get("CREDITO")),

                    # MENSAJE
                    asunto=self._clean(row.get("ASUNTO")),
                    mensaje=mensaje_final,

                    # DESTINATARIO
                    nombre_destinatario=self._clean(row.get("NOMBRE_DESTINATARIO")),
                    correo_destinatario=self._clean(row.get("CORREO_DESTINATARIO")),
                    identificacion_destinatario=self._clean(row.get("IDENTIFICACION_DESTINATARIO")),
                    nombre_del_destinatario=nombre_dest,
                    dias_mora_historicos=self._clean(row.get("DIASMORAHISTORICOS")),
                    ruta_pdf=f"/app/output/pdfs/memoriales/{self._clean(row.get('CREDITO'))}.pdf",
                    user=f"ECREDIT{user_counter}"

                )
                
                
                existe = await self.repository.documento_existe(conn,credito)

                if existe:
                    self.logger.info(f"El documento sí existe.{credito}")
                    continue
                else:
                  
                    proceedings_list.append(dto)

                user_counter += 1


        

            json_ready = [dto.model_dump() for dto in proceedings_list]

            with open("/app/output/base/proceedings.json", "w", encoding="utf-8") as f:
                json.dump(json_ready, f, ensure_ascii=False, indent=4)

            return proceedings_list

        except Exception as error:
            self.logger.exception(f"Error al procesar Excel: {error}")
            raise


    def _clean(self, value):
        if pd.isna(value):
            return ""
        value = str(value).strip()
        value = " ".join(value.split())  # <-- elimina espacios internos
        return value



    def _extract_surnames(self,nombre):
        partes = nombre.split()

        if len(partes) == 1:
            return partes[0]

        if len(partes) == 2:
            return partes[1]

        if len(partes) == 3:
            return " ".join(partes[-2:])

        # 4 palabras o más → todo después de las primeras dos
        return " ".join(partes[2:])
