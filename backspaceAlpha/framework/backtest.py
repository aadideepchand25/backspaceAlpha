from .loader import MultiDataFeed
from .broker import Broker
from .strategy import Strategy
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
from tqdm import tqdm
from datetime import datetime

class BaseBackTest:
    '''
    This class is used to bring everything together and run the backtest on it. The heart of the modular system
    Allows you to run the backtest on a strategy and provides some graphs to show results:
    - Portfolio Value vs Time               (shows overall how portfolio performed)
    - Portfolio Distribution vs Time        (shows PnL of different stocks in the portfolio over time)
    - Ticker Value vs Time                  (shows when trades were made on a ticker as its price changed)
    - Overall                               (shows results of the strategy (profit))
    - Will be adding more values and metrics soon...
    '''
    def __init__(self, strategy: Strategy, time_frame, start=10000, source="YAHOO", interval="1D", verbose=True, hedging=False, feed=None):
        self.start = start
        self.strategy = strategy
        self.verbose = verbose
        self.portfolio = self.strategy.portfolio
        self.broker = Broker(self.portfolio, start, verbose=verbose, hedging=hedging)
        self.strategy.broker = self.broker
        self.feed = MultiDataFeed(self.portfolio, time_frame, source, interval, feed)
        self.strategy.feed = self.feed
        self.strategy.init()
    
    def run(self, pbar = None):
        '''
        Heart of the backtest and does the basic loop:
        - Updates data feed by 1 tick
        - Sends data to broker first
        - Then strategy
        - Allows broker to respond to new orders from strategy
        '''
        if not self.verbose and pbar is None:
            pbar = tqdm(total=self.feed.feeds[0].length, ncols=70, desc="Running Backtest")
        while self.feed.has_next():
            data, rfr = self.feed.next()
            self.broker.update_price(data[:,3], rfr)
            self.strategy.update(data)
            self.broker.update()
            if not self.verbose:
                pbar.update(1)
        if not self.verbose and pbar is None:
            pbar.close()

class BackTest:
    def __init__(self, strategy, time_frame, start=10000, source="YAHOO", interval="1D", verbose=False, hedging=False, feed=None):
        self.backtests = []    
        self.verbose = verbose    
        strategy = strategy if isinstance(strategy, list) else [strategy]
        for strat in strategy:
            self.backtests.append(BaseBackTest(strat, time_frame, start, source, interval, verbose, hedging, feed))
        self.names = [x.strategy.name for x in self.backtests]
        if len(strategy) == 0:
            print("ERROR - Please ensure there are valid strategies to backtest")
            return
        start_dt = datetime.strptime(time_frame[0], '%Y-%m-%d')
        end_dt   = datetime.strptime(time_frame[1], '%Y-%m-%d')
        delta_days = (end_dt - start_dt).days
        self.years = delta_days / 365.25
        if interval == "1D":
            self.divisor = 252
        elif interval == "1W":
            self.divisor = 52
        elif interval == "1M":
            self.divisor = 12
        self.interval = interval
        if self.years <= 0:
            print("ERROR - Please ensure that a valid timeframe has been inputted")
            return
        if len(self.names) == 0:
            print("ERROR - Please ensure there are valid strategies to backtest")
            return
        pbar = None
        if not self.verbose:
            lengths = [x.feed.feeds[0].length for x in self.backtests]
            pbar = tqdm(total=np.sum(lengths), ncols=70, desc="Running Backtest")
        for backtest in self.backtests:
            backtest.run(pbar)
        if not self.verbose:
            pbar.close()

    def graph_variable(self, title, variable_names):
        plt.figure(figsize=(10, 5))
        variable_names = variable_names if isinstance(variable_names, list) else [variable_names]
        for variable in variable_names:
            if isinstance(variable["strategy"], str):
                variable["strategy"] = [variable["strategy"]]
            if isinstance(variable["variable"], str):
                variable["variable"] = [variable["variable"]]
            if len(variable["strategy"]) == 0:
                print("ERROR - Please ensure there are valid strategies to extract data from")
                return
            for name in variable["strategy"]:
                if name not in self.names:
                    print("ERROR - Please ensure the given strategy was present in the backtest")
                    return
                i = self.names.index(name)
                for variableName in variable["variable"]:
                    if variableName[:8] == "--ticker":
                        ticker = variableName[9:-1]
                        if ticker not in self.backtests[i].portfolio:
                            print("ERROR - Please ensure the given ticker is present in the strategy portfolio")
                            return
                        idx = self.backtests[i].portfolio.index(ticker)
                        data = [x["current"][idx] for x in self.backtests[i].broker.history]
                        plt.plot(data, label=f"{name} ({ticker})")
                        continue
                    if variableName[:7] == "--order":
                        if variableName[8:-1].count(")(") < 1:
                            print("ERROR - Please ensure the given anchor variable was formatted correctly")
                            return
                        ticker = variableName[8:-1].split(")(")[0]
                        variable = variableName[8:-1].split(")(")[1]
                        if variable not in self.backtests[i].broker.history[0] and variable != "":
                            print("ERROR - Please ensure the given anchor variable was present in the strategy")
                            return
                        orders = enumerate([x['orders'][ticker] for x in self.backtests[i].broker.history])
                        idx = self.backtests[i].portfolio.index(ticker)
                        data = [x["current"][idx] for x in self.backtests[i].broker.history]
                        if variable != "":
                            anchor = [x[variable] for x in self.backtests[i].broker.history]
                        else:
                            anchor = data
                        open = {}
                        distance = 0.2
                        for t, a in orders:
                            for order in a:
                                if order[0] == "B" or order[0] == "LNG":
                                    plt.scatter(t, anchor[t] - distance, marker='^', color='green', s=100)
                                elif order[0] == "S" or order[0] == "SHT":
                                    plt.scatter(t, anchor[t] + distance, marker='v', color='red', s=100)
                                
                                if order[0] == "LNG" or order[0] == "SHT":
                                    open[order[2]] = (t,order[0],order[5]) 
                                    continue
                                    
                                if order[0] == "CLS":
                                    start, action, price = open[order[1]]
                                    if action == "LNG":
                                        plt.plot([start, t], [anchor[start], anchor[start]], linestyle='--', color='green', linewidth=1.5)  
                                        if data[t] > price:
                                            plt.scatter(t, anchor[start]-distance, marker='^', color='green', s=100) 
                                        else:
                                            plt.scatter(t, anchor[start]+distance, marker='v', color='red', s=100)     
                                    else:
                                        plt.plot([start, t], [anchor[start], anchor[start]], linestyle='--', color='red', linewidth=1.5)  
                                        if data[t] < price:
                                            plt.scatter(t, anchor[start]+distance, marker='v', color='green', s=100) 
                                        else:
                                            plt.scatter(t, anchor[start]-distance, marker='^', color='red', s=100)
                                    del open[order[1]]
                                    continue
                                
                        t = len(data)-1
                        print(open.values())
                        for start, action, _ in open.values():
                            if action == "LNG":
                                plt.plot([start, t], [anchor[start], anchor[start]], linestyle='--', color='gray', linewidth=1.5) 
                            else: 
                                plt.plot([start, t], [anchor[start], anchor[start]], linestyle='--', color='gray', linewidth=1.5)
                        continue
                    if variableName not in self.backtests[i].broker.history[0]:
                        print("ERROR - Please ensure the given variable was present in the strategy")
                        return
                    data = [x[variableName] for x in self.backtests[i].broker.history]
                    plt.plot(data, label=f"{name} ({variableName})")
        plt.legend()
        plt.title(title)
        plt.xlabel("Time Step")
        plt.ylabel("Value")
        plt.grid(True)
        plt.show()
    
    def graph_function(self, title, func, args = [], kwargs = {}):
        plt.figure(figsize=(10, 5))
        for i in range(len(self.backtests)):
            data = self.backtests[i].broker.history
            y = func({"data": data, "interval": self.interval}, *args, **kwargs)
            plt.plot(y, label=self.names[i])
        plt.legend()
        plt.title(title)
        plt.xlabel("Time Step")
        plt.ylabel("Value")
        plt.grid(True)
        plt.show()

    def show_results(self):
        if len(self.names) == 0:
            print("ERROR - Please ensure there are valid strategies to backtest")
            return
        results = [ ["","Start [$]","Final [$]","Peak [$]","Profit [$]","Return [%]", "Return (Ann.) [%]", "Max Drawdown [%]", "Sharpe Ratio []", "Sharpe Ratio (Ann.) []"] ]
        for backtest in self.backtests:
            result = []
            data = [x["Equity"] for x in backtest.broker.history]
            result.append(backtest.strategy.name)
            result.append(backtest.start)
            final = data[len(backtest.broker.history)-1]
            result.append(final)
            result.append(max(data))
            result.append(final - backtest.start)
            result.append(((final - backtest.start)/backtest.start)*100)
            result.append((((final/backtest.start)**(1/self.years))-1)*100)
            running_max = np.maximum.accumulate(data)
            drawdowns = (data - running_max) / running_max
            result.append(drawdowns.min()*100)
            returns = np.diff(data) / data[:-1]
            rf = np.mean([x["Risk-Free Rate"] for x in backtest.broker.history]) / self.divisor
            if np.std(returns) != 0:
                sharpe_ratio = (np.mean(returns - rf)) / np.std(returns)
            else:
                sharpe_ratio = 0
            result.append(sharpe_ratio)
            result.append(sharpe_ratio * np.sqrt(self.divisor))
            results.append(result)
        data = list(zip(*results))
        spacing = np.max([len(x) for x in data[0]])
        spacing = max(spacing, 24)
        
        formatted = []        
        for row in data:
            new_row = []
            for val in row:
                if isinstance(val, (float, np.floating, int)):
                    new_row.append(f"{val:{spacing}.{5}{"g"}}")
                else:
                    new_row.append(str(val).ljust(spacing))  # pad strings
            formatted.append(new_row)
        
        tqdm.write("Backtest Complete - Outputting results\n")
        tqdm.write(" | ".join(formatted[0]) + " |")
        tqdm.write("-"*spacing + "-|-" + ("-"*spacing + "-+-")*(len(self.names)-1) + "-"*spacing + "-|")
        for row in formatted[1:]:
            tqdm.write(" | ".join(row) + " |")