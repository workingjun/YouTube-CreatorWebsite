from abc import ABC, abstractmethod

class IVideoDataManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self, table_name, data):
        pass

    @abstractmethod
    def fetch_all(self, table_name):
        pass



class IVideoIdManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self, table_name, data):
        pass

    @abstractmethod
    def fetch_all(self, table_name):
        pass

