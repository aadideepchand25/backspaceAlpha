from abc import ABC, abstractmethod

#Base Class for strategies
class Strategy(ABC):
    def __init__(self, portfolio, name):
        self.portfolio = portfolio
        self.broker = None
        self.feed = None
        self.name = name
    
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def update(self, data):
        pass