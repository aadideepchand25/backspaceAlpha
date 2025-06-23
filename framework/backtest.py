from loader import MultiDataFeed
from broker import Broker
import matplotlib.pyplot as plt

class BackTest:
    def __init__(self, strategy, time_frame, start=10000):
        self.strategy = strategy
        self.strategy.init()
        self.portfolio = self.strategy.portfolio
        self.broker = Broker(self.portfolio, start)
        self.strategy.broker = self.broker
        self.feed = MultiDataFeed(self.portfolio, time_frame)
    
    def run(self):
        while self.feed.has_next():
            data = self.feed.next()
            self.broker.update(data[:,3])
            self.strategy.update(data)
            self.broker.log()
            
    def show_portfolio(self):
        data = [x["value"] for x in self.broker.history]
        plt.figure(figsize=(10, 5))
        plt.plot(data)
        plt.title("Equity Curve")
        plt.xlabel("Time Step")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.show()
        
    def show_portfolio_distribution(self):
        data = [x["portfolio"] for x in self.broker.history]
        plt.figure(figsize=(10, 5))
        for stock in data:
            plt.plot(stock)
        plt.title("Portfolio Distribution")
        plt.xlabel("Time Step")
        plt.ylabel("Stock Value")
        plt.grid(True)
        plt.show()

    '''    
    def show_stock(self, ticker):
        i = self.portfolio.index(ticker)
        data = [x["current"][i] for x in self.broker.history]
        plt.figure(figsize=(10, 5))
        plt.plot(data)
        #plt.scatter(bx, by, marker='△', color='green', label='B', s=100)
        #plt.scatter(sx, sy, marker='▽', color='red', label='S', s=100)
        plt.title("Stock Value with Buys/Sells")
        pslt.xlabel("Time Step")
        plt.ylabel("Stock Value")
        plt.grid(True)
        plt.show()
    '''