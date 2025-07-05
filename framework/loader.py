import yfinance as yf
import numpy as np
from ib_insync import IB, Stock, util
import pandas as pd

#Iterator class
class BaseDataFeed:
    def has_next(self):
        raise NotImplementedError
    
    def next(self):
        raise NotImplementedError
    
    def previous(self):
        raise NotImplementedError

class YahooDataFeed(BaseDataFeed):
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

class IBKRDataFeed(BaseDataFeed):
    def __init__(self, symbol, time_frame, interval='1 min', host='127.0.0.1', port=7497, client_id=1):
        self.symbol = symbol
        self.start = time_frame[0]
        self.end = time_frame[1]
        self.interval = interval

        self.ib = IB()
        self.ib.connect(host, port, clientId=client_id)

        self.df = self._fetch_data()
        self.index = 0

    def _fetch_data(self):
        contract = Stock(self.symbol, 'SMART', 'USD')

        duration_map = {
            '1 min': '1 Y',
            '5 mins': '2 Y',
            '1 hour': '5 Y',
            '1 day': '20 Y'
        }

        duration = duration_map.get(self.interval, '1 Y')

        bars = self.ib.reqHistoricalData(
            contract,
            endDateTime='',
            durationStr=duration,
            barSizeSetting=self.interval,
            whatToShow='TRADES',
            useRTH=True,
            formatDate=1
        )

        if not bars:
            raise ValueError(f"No IBKR data for {self.symbol} in {self.interval}")

        df = util.df(bars)
        df = df.loc[(df['date'] >= self.start) & (df['date'] <= self.end)]
        df.reset_index(drop=True, inplace=True)
        return df

    def has_next(self):
        return self.index < len(self.df)

    def next(self):
        row = self.df.iloc[self.index]
        self.index += 1
        return row.to_numpy()

    def previous(self, num):
        start = max(0, self.index - num)
        return self.df.iloc[start:self.index].to_numpy()

    def disconnect(self):
        self.ib.disconnect()

class MultiDataFeed(BaseDataFeed):
    def __init__(self, portfolio, time_frame, source, interval):
        self.feeds = []
        for ticker in portfolio:
            if source == "IBKR":
                self.feeds.append(IBKRDataFeed(ticker, time_frame, interval))
            elif source == "YAHOO":
                self.feeds.append(YahooDataFeed(ticker, time_frame))
    
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