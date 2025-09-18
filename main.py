from strategies.PairsTradingStrategy import PairsTradingStrategy
import framework as f

'''
Quick example to show how to use the backtester to run the simulation and then show results
Can process a backtest of 5 years on a 1 day timeframe in about a few seconds with a large portfolio
'''

backtest = f.BackTest(PairsTradingStrategy(), ('2000-01-01', '2025-01-01'), 10000, "YAHOO", "1D", verbose=False)
backtest.run()
backtest.show_portfolio()
#backtest.show_portfolio_distribution()
backtest.show_results()
#backtest.show_stock("PEP")
#backtest.show_stock("KO")