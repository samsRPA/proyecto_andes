from dependency_injector import containers, providers
from app.domain.interfaces.IRabbitMQConsumer import IRabbitMQConsumer
from app.infrastucture.config.Settings import Settings
from app.infrastucture.rabbitmq.RabbitMQConsumer import RabbitMQConsumer
from app.application.services.ScrapperAndes import ScrapperAndes
from app.domain.interfaces.IScrapperAndes import IScrapperAndes





class Dependencies(containers.DeclarativeContainer):
  config = providers.Configuration()
  settings: providers.Singleton[Settings] = providers.Singleton(Settings)
  wiring_config = containers.WiringConfiguration(
    modules=[
      "main",
      ]
  )
    
  
    
    



    
  scrapper_andes: providers.Factory[IScrapperAndes] = providers.Factory(
    ScrapperAndes,
   
    
  )
  
    # Provider del consumidor
  rabbitmq_consumer: providers.Singleton[IRabbitMQConsumer] = providers.Singleton(
    RabbitMQConsumer,
    host=settings.provided.rabbitmq.HOST,
    port=settings.provided.rabbitmq.PORT,
    pub_queue_name=settings.provided.rabbitmq.PUB_QUEUE_NAME,
    prefetch_count=settings.provided.rabbitmq.PREFETCH_COUNT,
    user=settings.provided.rabbitmq.RABBITMQ_USER,
    password=settings.provided.rabbitmq.RABBITMQ_PASS,
    scrapper_andes=scrapper_andes.provider
  )
