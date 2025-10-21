from backspaceAlpha.framework import BackTest
from backspaceAlpha.examples import MeanReversionStrategy

'''
Quick example to show how to use the backtester to run the simulation and then show results
We use a simple Mean Reversion Strategy which in the example files runs on SPY
We choose to run the backtest over 25 years with a starting capital of $10,000
We then graph:
- the equity of the strategy over time 
- the SPY alongside our order markers
'''

#Run the backtest on the strategy
backtest = BackTest(MeanReversionStrategy(), ('2000-01-01', '2025-10-19'), 10000)

#Graphs the equity of the strategy over time
backtest.graph_variable("My Graph 1", {
    "strategy": "MeanReversionStrategy",
    "variable": "Equity"
})
#Graphs the SPY stock over time and order markers
backtest.graph_variable("My Graph 2", {
    "strategy": "MeanReversionStrategy",
    "variable": ["--ticker(SPY)", "--order(SPY)()"]
})

#Show results of the backtest
backtest.show_results()