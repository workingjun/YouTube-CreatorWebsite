from abc import ABC, abstractmethod

class ILinksManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self, table_name, data):
        pass

    @abstractmethod
    def fetch_all(self, table_name):
        pass