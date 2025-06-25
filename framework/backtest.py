from loader import MultiDataFeed
from broker import Broker
import matplotlib.pyplot as plt
import numpy as np

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
        data = np.array(data)
        plt.figure(figsize=(10, 5))
        for i in range(data.shape[1]):
            plt.plot(data[:, i], label=self.portfolio[i])
        plt.title("Portfolio Distribution")
        plt.xlabel("Time Step")
        plt.ylabel("Stock Value")
        plt.grid(True)
        plt.show()


    def show_stock(self, ticker):
        i = self.portfolio.index(ticker)
        data = [x["current"][i] for x in self.broker.history]
        orders = enumerate([filter(lambda a: a[1] == ticker, x["orders"]) for x in self.broker.history])
        plt.figure(figsize=(10, 5))
        plt.plot(data)
        for t, a in orders:
            for action, name, share in a:
                if action == "B":
                    plt.scatter(t, data[t] - 1, marker='^', color='green', label=share, s=100)
                elif action == "S":
                    plt.scatter(t, data[t] + 1, marker='v', color='red', label=share, s=100)
        plt.title(f"Stock Value with Buys/Sells - {ticker}")
        plt.xlabel("Time Step")
        plt.ylabel("Stock Value")
        plt.grid(True)
        plt.show()