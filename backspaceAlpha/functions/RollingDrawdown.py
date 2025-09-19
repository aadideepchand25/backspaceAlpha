import numpy as np

def RollingDrawdown(logs, window=-1):
    equity = np.array([x["Equity"] for x in logs["data"]])
    if window == -1:
        peak = np.maximum.accumulate(equity)
    else:
        if window >= len(equity):
            print("ERROR - Window size cannot be larger than the length of the data")
        peak = np.array([max(equity[max(0, i-window+1):i+1]) for i in range(len(equity))])
    drawdown = (equity - peak) / peak
    return drawdown*100