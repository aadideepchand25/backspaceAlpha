from framework import Strategy
import numpy as np

class PairsTradingStrategy(Strategy):
    def __init__(self):
        super().__init__(["PEP","KO"], self.__class__.__name__)
    
    def init(self):
        self.ols_window = 60
        self.threshold = 2
        self.exit = 0.5
        self.shares = 100
    
    def update(self, data):
        #Get close prices
        pepsi = data[0][3]
        cola = data[1][3]
        
        #Estimate hedge ratio
        pepsi_prev, cola_prev = self.feed.previous(self.ols_window)[:,:,3]
        beta_numerator = (len(pepsi_prev) * np.sum(pepsi_prev * cola_prev)) - (np.sum(pepsi_prev) * np.sum(cola_prev))
        beta_denominator = (len(pepsi_prev) * np.sum(pepsi_prev**2)) - (np.sum(pepsi_prev))**2
        beta = beta_numerator/beta_denominator
        alpha = (np.sum(cola_prev) - (beta * np.sum(pepsi_prev)))/len(pepsi_prev)
        
        #Get rolling spread 
        rolling_spread = cola_prev - (alpha + (beta * pepsi_prev))
        spread_mean = np.mean(rolling_spread)
        spread_std = np.std(rolling_spread)
        
        #Get current spread
        current_spread = cola - (alpha + (beta * pepsi))
        
        #Calculate Z-score
        z = (current_spread - spread_mean)/(spread_std)
        
        #Make trades
        if z > self.threshold:
            self.broker.short("KO", self.shares, "long_order")
            self.broker.long("PEP", self.shares * beta, "short_order")
        elif z < -self.threshold:
            self.broker.long("KO", self.shares, "long_order")
            self.broker.short("PEP", self.shares * beta, "short_order")
        elif z < self.exit and z > -self.exit:
            self.broker.close("long_order")
            self.broker.close("short_order")