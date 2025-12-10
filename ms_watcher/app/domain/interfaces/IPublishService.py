from abc import ABC, abstractmethod


class IPublishService(ABC):



    @abstractmethod
    async def publishProceedings(self):
        pass