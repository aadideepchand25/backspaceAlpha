from abc import ABC, abstractmethod
from .broker import Broker
from .loader import BaseDataFeed

#Base Class for strategies
class Strategy(ABC):
    def __init__(self, portfolio, name):
        self.portfolio = portfolio
        self.broker: Broker = None
        self.feed: BaseDataFeed = None
        self.name = name
    
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self, data):
        pass