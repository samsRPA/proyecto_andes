
from app.application.service.GetProceedingsService import GetProceedingsService
from app.application.service.PublishService import  PublishService


from app.domain.interfaces.IGetProceedingsService import IGetProceedingsService




from dependency_injector import containers, providers

from app.infrastucture.config.Settings import Settings
from app.domain.interfaces.IRabbitMQProducer import IRabbitMQProducer
from app.infrastucture.rabbitmq.RabbitMQProducer import RabbitMQProducer
from app.domain.interfaces.IPublishService import  IPublishService
from app.domain.interfaces.IDataBase import IDataBase
from app.infrastucture.database.OracleDB import OracleDB
from app.infrastucture.database.repositories.DocumentRepository import DocumentRepository


class Dependencies(containers.DeclarativeContainer):
  config = providers.Configuration()
  settings: providers.Singleton[Settings] = providers.Singleton(Settings)
  wiring_config = containers.WiringConfiguration(
     modules=["app.api.routes.proceeding_andes_routes"]
  )


  data_base: providers.Singleton[IDataBase] = providers.Singleton(
        OracleDB,
        db_user=settings.provided.data_base.DB_USER,
        db_password=settings.provided.data_base.DB_PASSWORD,
        db_host=settings.provided.data_base.DB_HOST,
        db_port=settings.provided.data_base.DB_PORT,
        db_service_name=settings.provided.data_base.DB_SERVICE_NAME,
    )



  document_repository= providers.Factory(
        DocumentRepository,
       
    )


   
  get_data_service: providers.Factory[IGetProceedingsService] = providers.Factory(
      GetProceedingsService,
    document_repository,

      
    )



  rabbitmq_producer: providers.Singleton[IRabbitMQProducer] = providers.Singleton(
        RabbitMQProducer,
        host=settings.provided.rabbitmq.HOST,
        port=settings.provided.rabbitmq.PORT,
        pub_queue_name=settings.provided.rabbitmq.PUB_QUEUE_NAME,
        user=settings.provided.rabbitmq.RABBITMQ_USER,
        password=settings.provided.rabbitmq.RABBITMQ_PASS
    )
 
  publish_service:  providers.Factory[IPublishService] = providers.Factory(
      PublishService,
      get_data_service,
      rabbitmq_producer,
      data_base
    )
