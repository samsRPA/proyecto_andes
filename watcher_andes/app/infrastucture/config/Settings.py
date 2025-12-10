from pydantic_settings import BaseSettings


from app.infrastucture.config.RabbitMQSettings import RabbitMQSettings
from app.infrastucture.config.BrowserConfig import BrowserConfig

class Settings(BaseSettings):
    browser:BrowserConfig = BrowserConfig()
    rabbitmq : RabbitMQSettings = RabbitMQSettings()

def load_config() -> Settings:
    return Settings()
