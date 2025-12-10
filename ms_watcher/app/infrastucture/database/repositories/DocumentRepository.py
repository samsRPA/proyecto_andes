import asyncio
import logging

class DocumentRepository:

    logger = logging.getLogger(__name__)
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def documento_existe(self, conn, parte_nombre: str) -> bool:
        """
        Verifica si existe un documento en la tabla ARCHIVOS_ENVIADOS_ANDES
        buscando por coincidencia en el campo nombre_archivo usando LIKE.
        """
        try:
            query = """
                SELECT 1
                FROM ARCHIVOS_ENVIADOS_ANDES
                WHERE nombre_archivo = :patron
                FETCH FIRST 1 ROWS ONLY
            """

            async def _execute():
                async with conn.cursor() as cursor:
                    await cursor.execute(query, {
                        "patron": f"{parte_nombre}.pdf"
                    })
                    row = await cursor.fetchone()
                    return row

            result = await _execute()
            return result is not None

        except Exception as error:
            self.logger.error(f"❌ Error en documento_existe: {error}")
            raise


