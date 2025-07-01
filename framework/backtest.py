from loader import MultiDataFeed
from broker import Broker
from strategy import Strategy
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

class BackTest:
    def __init__(self, strategy: Strategy, time_frame, start=10000):
        self.start = start
        self.strategy = strategy
        self.strategy.init()
        self.portfolio = self.strategy.portfolio
        self.broker = Broker(self.portfolio, start)
        self.strategy.broker = self.broker
        self.feed = MultiDataFeed(self.portfolio, time_frame)
        self.strategy.feed = self.feed
    
    def run(self):
        first = True
        while self.feed.has_next():
            data = self.feed.next()
            self.broker.update_price(data[:,3])
            self.strategy.update(data)
            self.broker.update()
            
    def show_portfolio(self):
        data = [x["equity"] for x in self.broker.history]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data)
        formatter = ScalarFormatter(useOffset=False)
        ax.yaxis.set_major_formatter(formatter)
        plt.title(f"{self.strategy.name} - Portfolio Value")
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
        plt.title(f"{self.strategy.name} - Portfolio Distribution")
        plt.xlabel("Time Step")
        plt.ylabel("PnL of Open Positions")
        plt.grid(True)
        plt.show()


    def show_stock(self, ticker):
        distance = 0.2
        i = self.portfolio.index(ticker)
        data = [x["current"][i] for x in self.broker.history]
        orders = enumerate([x['orders'][ticker] for x in self.broker.history])
        open = {}
        plt.figure(figsize=(10, 5))
        plt.plot(data)
        for t, a in orders:
            for order in a:
                if order[0] == "B" or order[0] == "LNG":
                    plt.scatter(t, data[t] - distance, marker='^', color='green', label=order[1], s=100)
                elif order[0] == "S" or order[0] == "SHT":
                    plt.scatter(t, data[t] + distance, marker='v', color='red', label=order[1], s=100)
                   
                if order[0] == "LNG" or order[0] == "SHT":
                    open[order[2]] = (t,order[0],order[5]) 
                    
                if order[0] == "CLS":
                    start, action, price = open[order[1]]
                    if action == "LNG":
                        plt.plot([start, t], [price, price], linestyle='--', color='green', linewidth=1.5)  
                        if data[t] > price:
                            plt.scatter(t, price-distance, marker='^', color='green', s=100) 
                        else:
                            plt.scatter(t, price+distance, marker='v', color='red', s=100)     
                    else:
                        plt.plot([start, t], [price, price], linestyle='--', color='red', linewidth=1.5)  
                        if data[t] < price:
                            plt.scatter(t, price+distance, marker='v', color='green', s=100) 
                        else:
                            plt.scatter(t, price-distance, marker='^', color='red', s=100)
                    del open[order[1]]
        t = len(data)-1
        for id, o in open.items():
            start, action, price = o
            if action == "LNG":
                plt.plot([start, t], [price, price], linestyle='--', color='gray', linewidth=1.5) 
            else: 
                plt.plot([start, t], [price, price], linestyle='--', color='gray', linewidth=1.5)
        plt.title(f"Stock Value with Buys/Sells - {ticker}")
        plt.xlabel("Time Step")
        plt.ylabel("Stock Value")
        plt.grid(True)
        plt.show()
        
    def show_results(self):
        final = self.broker.history[len(self.broker.history)-1]
        print(f"\n\nRESULTS - {self.strategy.name}:")
        print(f"Profit: £{final['equity']-self.start}")