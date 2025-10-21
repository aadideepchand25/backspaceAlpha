# backspaceAlpha

[![License](https://img.shields.io/badge/license-BackspaceAlpha-blue.svg)](./LICENSE)
[![PyPI](https://img.shields.io/pypi/v/backspaceAlpha.svg)](https://pypi.org/project/backspaceAlpha/)

A simple, customisable, easy-to-use backtesting framework with example strategies to quickly and effectively track a strategies' impact and improve it

### Contents:
1. [Overview](#1-overview)
2. [Installation](#2-installation)
3. [Usage](#3-usage)
4. [Documentation](#4-documentation)
    1. [Framework](#4.1-framework)
    2. [Functions](#4.2-functions)



## 1. Overview
backspaceAlpha is a backtesting framework, that aims to improve customisability and simplify the backtesting process by implementing functionality in the same way as real trading. It does this by having a small number of incredibly versatile functions/classes and splitting the functionality between 4 main modules:

- **backtester** - Handles all things related to running the backtest and displaying its resuls
- **broker** - Operates in the same way as a real broker, by maintaining an order book and handling order conflicts
- **loader** - Operates in the same way as a market data provider by aggregating data from exchanges and sending them to brokers in an intuitive format
- **strategy** - Handles all things related to what a strategy may entail

It is aimed at everyone from trading beginners to industry veterans and provides many useful examples for a range of strategies, to help users understand the framework. It is designed to be intuitive and allow for new users to start experimenting with functions and customisability quickly

## 2. Installation
This project is available on PyPi at the following [link](https://pypi.org/project/backspaceAlpha/) and can be installed with:
```python
$ pip install backspaceAlpha
```

## 3. Usage
The easiest way to get started with backspaceAlpha is to import strategies from the example folder and run backtests on them. This can be done as demonstrated by the files in this [folder](https://github.com/aadideepchand25/backspaceAlpha/tree/main/test) or as shown below:

```python
from backspaceAlpha.framework import BackTest
from backspaceAlpha.examples import MeanReversionStrategy

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
```

In this example, we use a simple [mean reversion strategy](https://github.com/aadideepchand25/backspaceAlpha/blob/main/backspaceAlpha/examples/MeanReversionStrategy.py) which is predefined in the example folder to run on SPY. We choose to run the backtest over 25 years with a starting capital of $10,000. After the backtest completes, we then graph:

- the equity of the strategy over time 
- the SPY alongside our order markers

We then show the results of the backtest which will include metrics such as profit, return, max drawdown, sharpe ratio etc.

## 4. Documentation
In this section, we go in depth into the workings of the backtester and how each component of each script works. We split it by folder and within each folder, we explore the functions of each script
### 4.1 - Framework
This section includes scripts with the main functionality of the backtester. It is split into different scripts in the same way discussed in the [overview](#1-overview))

### 4.2 - Functions

## Attribution
This software is licensed under the **[BackspaceAlpha License v1.0](https://github.com/aadideepchand25/backspaceAlpha/blob/main/LICENSE)**.  
Use of this software requires attribution
Modifications must be submitted via the official GitHub repository.