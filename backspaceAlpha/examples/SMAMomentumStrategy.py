from backspaceAlpha.framework import Strategy
import numpy as np

#Define our SMA Momentum Signals and make sure it inherits from backspaceAlpha's Strategy class
class SMAMomentumStrategy(Strategy):
    def __init__(self):
        #Define the tickers our strategy intends to use and the name of the strategy
        super().__init__(["SPY"], "SMAMomentumStrategy")

    def init(self):
        #We use this init() function to define variables our strategy will use
        self.shortWindow = 30
        self.longWindow = 60
        #We also prepare to log our two SMA variables so we can graph them later
        self.log("SMA - Long")
        self.log("SMA - Short")
        
        #This variable will be used to keep track of previous state
        self.previousDifference = 0

        #Define our take profit and stop loss values as well as how many shares to trade each time
        self.shares = 5
        self.takeProfit = 0.1
        self.stopLoss = 0.05

    def update(self, data):
        #Every tick, we make sure to fetch the previous data from our data feed and get the close price
        window1 = self.feed.previous(self.longWindow)[:,:,3]
        window2 = self.feed.previous(self.shortWindow)[:,:,3]
        #We compute the mean across these windows
        sma1 = np.mean(window1)
        sma2 = np.mean(window2)
        
        #We then log these variables to graph
        self.log("SMA - Long", sma1)
        self.log("SMA - Short", sma2)
        
        #Calculates difference between the SMAs
        difference = sma1 - sma2

        #Gets the close price
        price = data[0][3]

        #Checks for change in sign and excludes ticks where difference=0
        if difference * self.previousDifference < 0 and difference != 0:
        
            #Checks if this crossover is a buy signal
            if difference < 0:
                #Calculates the take profit and stop loss for this price
                tp = price + (price * self.takeProfit)
                sl = price - (price * self.stopLoss)
                #Makes the trade
                self.broker.long(self.portfolio[0], self.shares, "long-order", tp, sl)

            #Checks if this crossover is a sell signal
            if difference > 0:
                #Calculates the take profit and stop loss for this price
                tp = price - (price * self.takeProfit)
                sl = price + (price * self.stopLoss)
                #Makes the trade
                self.broker.short(self.portfolio[0], self.shares, "short-order", tp, sl)
        
        #Updates our previous difference if we are not currently at a crossover
        if difference != 0:
            self.previousDifference = difference