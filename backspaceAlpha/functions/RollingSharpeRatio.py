import numpy as np

def RollingSharpeRatio(logs, window=-1, annualized=True):
    interval = logs["interval"]
    if interval == "1D":
        divisor = 252
    elif interval == "1W":
        divisor = 52
    elif interval == "1M":
        divisor = 12
            
    equity = np.array([x["Equity"] for x in logs["data"]])
    rfr = np.array([x["Risk-Free Rate"] for x in logs["data"]]) / divisor
    rfr = rfr[1:]
    returns = np.diff(equity) / equity[:-1]
    
    if window >= len(equity):
        print("ERROR - Window size cannot be larger than the length of the data")
    
    if window == -1:
        rfr = np.array([np.mean(rfr[:i+1]) for i in range(len(rfr))])
        mean = np.array([np.mean(returns[:i+1]) for i in range(len(returns))])
        std = np.array([np.std(returns[:i+1]) for i in range(len(returns))])
    else:
        rfr = np.array([np.mean(rfr[max(0, i-window+1):i+1]) for i in range(len(rfr))])
        mean = np.array([np.mean(returns[max(0, i-window+1):i+1]) for i in range(len(returns))])
        std = np.array([np.std(returns[max(0, i-window+1):i+1]) for i in range(len(returns))])
    
    sharpe_ratio = np.divide(
        mean - rfr,
        std,
        out=np.full_like(std, np.nan, dtype=np.float64),
        where=std != 0
    )
    
    if annualized:
        sharpe_ratio *= np.sqrt(divisor)
    return sharpe_ratio