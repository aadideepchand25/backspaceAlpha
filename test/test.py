from backspaceAlpha.framework import BackTest
from backspaceAlpha.functions import RollingDrawdown, RollingSharpeRatio
from backspaceAlpha.examples import PairsTradingStrategy, MeanReversionStrategy, BuyAndHoldSPYStrategy, SMAMomentumStrategy

'''
Quick example to show how to use the backtester to run the simulation and then show results
Can process a backtest of 5 years on a 1 day timeframe in about a few seconds with a large portfolio
'''

#Run the backtest on multiple strategies simultaneously
strategies = [PairsTradingStrategy(),MeanReversionStrategy(),BuyAndHoldSPYStrategy()]
#backtest = BackTest(strategies, ('2000-01-01', '2025-01-01'), 10000, "YAHOO", "1W", verbose=True)

backtest2 = BackTest([SMAMomentumStrategy()], ('2025-01-01', '2025-06-01'), verbose=True)

#Graphs our variables along side the ticker
backtest2.graph_variable("SMA Momentum Strategy (Test)", {
    "strategy": "SMAMomentumStrategy",
    "variable": ["SMA - Long", "SMA - Short", "--ticker(SPY)", "--order(SPY)(SMA - Short)"]
})

#Show graphs for the results of the backtest
'''
backtest.graph_variable("Portfolio Equity", [{
    "strategy": ["PairsTradingStrategy", "MeanReversionStrategy"], 
    "variable": "Equity"
},{
    "strategy": ["BuyAndHoldSPYStrategy"], 
    "variable": ["--order(SPY)(Equity)", "Equity"]
}])
backtest.graph_function("Rolling Drawdown", RollingDrawdown, args=[-1])
backtest.graph_function("Rolling Sharpe Ratio", RollingSharpeRatio, args=[-1])
backtest.graph_stock("MeanReversionStrategy", "SPY")
backtest.graph_stock("BuyAndHoldSPYStrategy", "SPY")

#Show results of the backtest
backtest.show_results()
'''