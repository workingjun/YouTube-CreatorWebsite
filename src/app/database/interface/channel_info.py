from abc import ABC, abstractmethod

class IChannelInfoManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self, data):
        pass

    @abstractmethod
    def fetch_one(self, title):
        pass

    @abstractmethod
    def fetch_all(self):
        pass