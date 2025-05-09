from abc import ABC, abstractmethod

class ILinksManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self):
        pass

    @abstractmethod
    def fetch_all(self):
        pass

    def fetch_one(self):
        pass