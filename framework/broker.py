class Broker:
    def __init__(self, portfolio, initial, hedging = True):
        self.cash = initial
        self.tickers = portfolio
        self.portfolio = dict.fromkeys(portfolio, 0)
        self.price = dict.fromkeys(portfolio, 0)
        self.history = []
        self.order = {ticker: [] for ticker in portfolio}
        self.open = {ticker: [] for ticker in portfolio}
        self.hedging = hedging
        
    def update(self, data):
        self.price = dict(zip(self.tickers, data))
        
        #Handle current orderbook state
        for t, orders in self.order.items():
            actions = [o[0] for o in orders]
            if ("B" in actions and "S" in actions):
                print(f"ERROR - Could not process order book ({t}): Attempting to buy and sell simultaneously")
                return
            if not self.hedging and ("LNG" in actions and "SHT" in actions) or ("B" in actions and "SHT" in actions) or ("S" in actions and "LNG" in actions):
                print(f"ERROR - Could not process order book ({t}): Attempting illegal operation without hedging mode")
                return
            buy = sum([o[1] for o in orders if o[0] == "B"])
            long = [o for o in orders if o[0] == "LNG"]
            sell = sum([o[1] for o in orders if o[0] == "S"])  
            short = [o for o in orders if o[0] == "SHT"]
            price = self.price[t]
            if self.cash >= (buy + sum([l[1] for l in long]) + (sum([s[1] for s in short]) * 1.5)) * price and self.portfolio[t] + buy >= sell:
                self.cash += (sell - buy + sum([s[1] for s in short]) - sum([l[1] for l in long])) * price
                self.portfolio[t] += (buy - sell)
                self.open[t] += short + long
                self.order[t] = []
                continue
            print(f"ERROR - Could not process order book ({t}): Invalid cash or shares to execute orderbook")
   
    def buy(self, ticker, share):
        self.order[ticker].append(("B", share))
    
    def sell(self, ticker, share):
        self.order[ticker].append(("S", share))     
            
    def long(self, ticker, share, id, tp, sl):
        if not self.hedging and "SHT" in [o[0] for o in self.open[ticker]]:
            print("ERROR - Could not process order book: Attempting to maintain long and short position without hedging mode")
        else:
            self.order[ticker].append(("LNG", share, id, float(tp), float(sl), self.price[ticker]))
            
    def short(self, ticker, share, id, tp, sl):
        if not self.hedging and "LNG" in [o[0] for o in self.open[ticker]]:
            print("ERROR - Could not process order book: Attempting to maintain long and short position without hedging mode")
        else:
            self.order[ticker].append(("SHT", share, id, float(tp), float(sl), self.price[ticker]))

    def value(self):
        value = sum([self.portfolio[t] * self.price[t] for t in self.tickers])
        for t in self.tickers:
            price = self.price[t]
            for p in self.open[t]:
                if p[0] == "SHT":
                    value += (p[5] - price) * p[1]
                elif p[0] == "LNG":
                    value += (price - p[5]) * p[1]
        return value

    def log(self):
        self.history.append({
            'equity': self.cash + self.value(),
            'portfolio': self.value(),
            'current': [self.price[t] for t in self.tickers],
            'orders': self.order
        })