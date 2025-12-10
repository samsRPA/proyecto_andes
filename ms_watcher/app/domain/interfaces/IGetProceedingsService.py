from abc import ABC, abstractmethod
 


class IGetProceedingsService(ABC):


    @abstractmethod
    async def get_proceedings(self,conn):
        pass