from abc import ABC, abstractmethod

class IVideoDataManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self):
        pass

    @abstractmethod
    def fetch_all(self):
        pass



class IVideoIdManager(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def upsert_data(self):
        pass

    @abstractmethod
    def fetch_all(self):
        pass

