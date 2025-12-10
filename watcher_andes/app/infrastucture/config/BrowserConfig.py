from pydantic import Field
from app.infrastucture.config.EnvConfig import EnvConfig


class BrowserConfig(EnvConfig):
    USER:str = Field(..., alias="USER")
    PASSWORD:str = Field(..., alias="PASSWORD")
    URL_LOGIN: str = Field(..., alias="URL_LOGIN")
    #URL_API_CONVALIDACIONES:str = Field(..., alias="URL_API_CONVALIDACIONES")
    #URL_API_ACTIVITY: str = Field(..., alias="URL_API_ACTIVITY")

    
