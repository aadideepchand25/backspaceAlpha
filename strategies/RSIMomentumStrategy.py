from framework import Strategy
import numpy as np

class RSIMomentumStrategy(Strategy):
    def __init__(self):
        super().__init__(["PEP","KO"], self.__class__.__name__)
        self.period = 14
        self.rsi_values = {ticker: [] for ticker in ["PEP","KO"]}
        self.position_open = False
        self.position_id_long = None
        self.position_id_short = None
        self.tp_sl_pct = 0.05  # 5%
    
    def init(self):
        pass
    
    def compute_rsi(self, prices):
        deltas = np.diff(prices)
        seed = deltas[:self.period]
        up = seed[seed >= 0].sum() / self.period
        down = -seed[seed < 0].sum() / self.period
        rs = up / down if down != 0 else 0
        rsi = 100 - 100 / (1 + rs)
        rsi_values = [rsi]
        up_avg = up
        down_avg = down
        
        for delta in deltas[self.period:]:
            up_val = max(delta, 0)
            down_val = -min(delta, 0)
            up_avg = (up_avg * (self.period - 1) + up_val) / self.period
            down_avg = (down_avg * (self.period - 1) + down_val) / self.period
            rs = up_avg / down_avg if down_avg != 0 else 0
            rsi = 100 - 100 / (1 + rs)
            rsi_values.append(rsi)
        return rsi_values
    
    def update(self, data):
        close_prices = data[:, 3]
        tickers = self.portfolio
        
        for i, ticker in enumerate(tickers):
            self.rsi_values[ticker].append(close_prices[i])
            if len(self.rsi_values[ticker]) < self.period + 1:
                return  # Wait for enough data
        
        rsi1 = self.compute_rsi(self.rsi_values[tickers[0]])[-1]
        rsi2 = self.compute_rsi(self.rsi_values[tickers[1]])[-1]
        spread = rsi1 - rsi2
        
        # Entry threshold for spread
        entry_threshold = 7
        exit_threshold = 3
        
        if not self.position_open:
            if spread > entry_threshold:
                # RSI1 overbought relative to RSI2, short ticker1, long ticker2
                shares1 = int(self.broker.cash / 2 / close_prices[0])
                shares2 = int(self.broker.cash / 2 / close_prices[1])
                if shares1 > 0 and shares2 > 0:
                    tp1 = close_prices[0] * (1 - self.tp_sl_pct)
                    sl1 = close_prices[0] * (1 + self.tp_sl_pct)
                    tp2 = close_prices[1] * (1 + self.tp_sl_pct)
                    sl2 = close_prices[1] * (1 - self.tp_sl_pct)
                    id1 = f"{tickers[0]}_short_{self.broker.time}"
                    id2 = f"{tickers[1]}_long_{self.broker.time}"
                    self.broker.short(tickers[0], shares1, id1, tp1, sl1)
                    self.broker.long(tickers[1], shares2, id2, tp2, sl2)
                    self.position_open = True
                    self.position_id_short = id1
                    self.position_id_long = id2
            elif spread < -entry_threshold:
                # RSI1 oversold relative to RSI2, long ticker1, short ticker2
                shares1 = int(self.broker.cash / 2 / close_prices[0])
                shares2 = int(self.broker.cash / 2 / close_prices[1])
                if shares1 > 0 and shares2 > 0:
                    tp1 = close_prices[0] * (1 + self.tp_sl_pct)
                    sl1 = close_prices[0] * (1 - self.tp_sl_pct)
                    tp2 = close_prices[1] * (1 - self.tp_sl_pct)
                    sl2 = close_prices[1] * (1 + self.tp_sl_pct)
                    id1 = f"{tickers[0]}_long_{self.broker.time}"
                    id2 = f"{tickers[1]}_short_{self.broker.time}"
                    self.broker.long(tickers[0], shares1, id1, tp1, sl1)
                    self.broker.short(tickers[1], shares2, id2, tp2, sl2)
                    self.position_open = True
                    self.position_id_long = id1
                    self.position_id_short = id2
        else:
            # Close positions if spread near zero
            if abs(spread) < exit_threshold:
                self.broker.close(self.position_id_long)
                self.broker.close(self.position_id_short)
                self.position_open = False
                self.position_id_long = None
                self.position_id_short = None
