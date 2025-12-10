

from app.domain.interfaces.IGetProceedingsService import IGetProceedingsService

import logging
from app.domain.interfaces.IRabbitMQProducer import IRabbitMQProducer
from app.application.dto.ProceedingsDto import ProceedingsDto
from app.domain.interfaces.IPublishService import IPublishService
from app.domain.interfaces.IDataBase import IDataBase



class PublishService(IPublishService):

    logger= logging.getLogger(__name__)
   
    def __init__(self,  getData:IGetProceedingsService, producer: IRabbitMQProducer,db:IDataBase):
        self.getData = getData
        self.producer= producer
        self.db=db
     
    async def getAllProceedings(self,conn):
     
        try:
            
            raw_proceedings = await  self.getData.get_proceedings(conn)
            if raw_proceedings:
                self.logger.info(f"✅ Se extrayeron {len(raw_proceedings)} expedientes")
            return raw_proceedings
        except Exception as e:
            self.logger.error(f"❌ Error : {e}")
            raise e
 

    async def publishProceedings(self):
       
        try:
            conn = await self.db.acquire_connection()
            proceedings= await self.getAllProceedings(conn)
            

            if not proceedings:
                raise ValueError("No hay radicados para publicar")
                
            for proceeding in proceedings:
              
    
                await self.producer.publishMessage(proceeding.dict())
 
        except Exception as error:
            logging.exception(f"Error al publicar {error}")
            raise error 
        finally:
            await  self.db.release_connection(conn)
       
    
