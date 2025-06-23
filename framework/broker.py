class Broker:
    def __init__(self, portfolio, inital):
        self.cash = initial
        self.tickers = portfolio
        self.portfolio = dict.fromkeys(portfolio, 0)
        self.current = self.portfolio
        self.history = []
        self.order = []
        
    def update(self, data):
        self.current = dict.fromkeys(self.tickers, data)
        
    def buy(self, ticker, share):
        price = self.current[ticker] * share
        if self.cash > price:
            self.cash -= price
            self.portfolio[ticker] += price
            self.order.append(("B", ticker, share))
    
    def sell(self, ticker, share):
        price = self.current[ticker] * share
        if self.portfolio[ticker] > price:
            self.portfolio[ticker] -= price
            self.cash += price
            self.order.append(("S", ticker, share))
            
    def log(self):
        self.history.append({
            'value': self.cash + sum(self.portfolio.values()),
            'portfolio': self.portfolio.values(),
            'current': self.current.values(),
            'orders': self.order
        })
        self.order = []