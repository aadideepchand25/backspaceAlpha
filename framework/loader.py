import yfinance as yf
import numpy as np

#Iterator class
class DataFeed:
    def __init__(self, symbol, time_frame):
        data = yf.download(symbol, start=time_frame[0], end=time_frame[1], auto_adjust=True)
        self.df = data.reset_index(drop=True)
        self.index = 0
        self.length = len(self.df)

    def has_next(self):
        return self.index < self.length

    def next(self):
        row = self.df.iloc[self.index]
        self.index += 1
        return row.to_numpy()
    
    def previous(self, num):
        start = max(0, self.index - num)
        sub_df = self.df.iloc[start:self.index]
        return sub_df.to_numpy()
    

class MultiDataFeed:
    def __init__(self, portfolio, time_frame):
        self.feeds = []
        for ticker in portfolio:
            self.feeds.append(DataFeed(ticker, time_frame))
    
    def has_next(self):
        return all(feed.has_next() for feed in self.feeds)  
        
    def next(self):
        out = np.zeros((len(self.feeds), 5))
        for i, feed in enumerate(self.feeds):
            out[i, :] = feed.next()
        return out
            
    def previous(self, num):
        a = max(0, min([x.index for x in self.feeds])-num)
        out = np.zeros((len(self.feeds), a, 5))
        for i, feed in enumerate(self.feeds):
            out[i,:,:] = feed.previous(a)
        return out