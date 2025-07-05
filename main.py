from strategies.RSIMomentumStrategy import RSIMomentumStrategy
import framework as f

backtest = f.BackTest(RSIMomentumStrategy(), ('2000-01-01', '2025-06-20'), 10000, "YAHOO", "1D", verbose=False)
backtest.run()
backtest.show_portfolio()
backtest.show_portfolio_distribution()
backtest.show_results()