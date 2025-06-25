class Broker:
    def __init__(self, portfolio, initial):
        self.cash = initial
        self.tickers = portfolio
        self.portfolio = dict.fromkeys(portfolio, 0)
        self.current = self.portfolio
        self.history = []
        self.order = []
        
    def update(self, data):
        self.current = dict(zip(self.tickers, data))
        
    def buy(self, ticker, share):
        price = self.current[ticker] * share
        if self.cash > price:
            self.cash -= price
            self.portfolio[ticker] += share
            self.order.append(("B", ticker, share))
    
    def sell(self, ticker, share):
        price = self.current[ticker] * share
        if self.portfolio[ticker] >= share:
            self.portfolio[ticker] -= share
            self.cash += price
            self.order.append(("S", ticker, share))
            
    def log(self):
        value = [self.portfolio[ticker] * self.current[ticker] for ticker in self.tickers]
        self.history.append({
            'value': self.cash + sum(value),
            'portfolio': value,
            'current': [self.current[t] for t in self.tickers],
            'orders': self.order
        })
        self.order = []