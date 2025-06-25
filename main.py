import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# === Data Feed ===
class DataFeed:
    def __init__(self, df):
        self.df = df.reset_index(drop=True)
        self.index = 0
        self.length = len(df)

    def has_next(self):
        return self.index < self.length

    def next(self):
        row = self.df.iloc[self.index]
        self.index += 1
        return row.to_dict()


# === Broker / Portfolio Simulator ===
class Broker:
    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.position = 0
        self.trades = []
        self.history = []

    def buy(self, price):
        if self.cash >= price:
            self.position += 1
            self.cash -= price
            self.trades.append(('BUY', price))

    def sell(self, price):
        if self.position > 0:
            self.position -= 1
            self.cash += price
            self.trades.append(('SELL', price))

    def log(self, price):
        portfolio_value = self.cash + self.position * price
        self.history.append({
            'cash': self.cash,
            'position': self.position,
            'portfolio_value': portfolio_value
        })


# === Strategy Base Class ===
class Strategy:
    def __init__(self, data_feed, broker):
        self.data = data_feed
        self.broker = broker

    def init(self):
        pass

    def next(self, bar):
        raise NotImplementedError


# === Example Strategy: SMA Crossover ===
class SMACrossoverStrategy(Strategy):
    def init(self):
        self.prices = []

    def next(self, bar):
        self.prices.append(bar['Close'])
        if len(self.prices) < 20:
            return

        short_sma = np.mean(self.prices[-5:])
        long_sma = np.mean(self.prices[-20:])

        if short_sma > long_sma:
            self.broker.buy(bar['Close'])
        elif short_sma < long_sma:
            self.broker.sell(bar['Close'])


# === Backtesting Engine ===
def run_backtest(strategy_class, data):
    feed = DataFeed(data)
    broker = Broker()
    strategy = strategy_class(feed, broker)

    strategy.init()
    while feed.has_next():
        bar = feed.next()
        strategy.next(bar)
        broker.log(bar['Close'])

    return broker


# === Plotting ===
def plot_results(broker):
    values = [x['portfolio_value'] for x in broker.history]
    plt.figure(figsize=(10, 5))
    plt.plot(values)
    plt.title("Equity Curve")
    plt.xlabel("Time Step")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.show()


# === Main Run ===
if __name__ == "__main__":
    symbol = "AAPL"
    data = yf.download(symbol, start="2022-01-01", end="2022-12-31", auto_adjust=True)
    data = data.xs(symbol, axis=1, level=1)

    broker = run_backtest(SMACrossoverStrategy, data)
    plot_results(broker)

    # Optional summary
    final_value = broker.history[-1]['portfolio_value']
    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Total Trades: {len(broker.trades)}")
