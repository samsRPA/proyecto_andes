from abc import ABC, abstractmethod


class IScrapperAndes(ABC):

    # @abstractmethod
    # async def start_login(self):
    #     pass



    @abstractmethod
    def runScrapper(self):
        pass
    
    

