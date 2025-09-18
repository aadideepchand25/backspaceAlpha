from strategies.BuyAndHoldSPYStrategy import BuyAndHoldSPYStrategy
from strategies.MeanReversionStrategy import MeanReversionStrategy
from strategies.PairsTradingStrategy import PairsTradingStrategy
import framework as f

'''
Quick example to show how to use the backtester to run the simulation and then show results
Can process a backtest of 5 years on a 1 day timeframe in about a few seconds with a large portfolio
'''

#Run the backtest on multiple strategies simultaneously
strategies = [PairsTradingStrategy(),MeanReversionStrategy(),BuyAndHoldSPYStrategy()]
backtest = f.MultiBackTest(strategies, ('2000-01-01', '2025-01-01'), 10000, "YAHOO", "1D", verbose=False)
backtest.run()

#Show graphs for the results of the backtest
backtest.show_portfolio()
backtest.show_stock("MeanReversionStrategy", "SPY")
backtest.show_stock("BuyAndHoldSPYStrategy", "SPY")

#Show results of the backtest
backtest.show_results()