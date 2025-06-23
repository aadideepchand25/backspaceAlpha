#Base Class for strategies
class Strategy:
    def __init__(self):
        self.portfolio = []
        self.broker = None
        
    def init(self):
        pass

    def update(self, data):
        raise NotImplementedError 