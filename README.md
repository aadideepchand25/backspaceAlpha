# backspaceAlpha

[![License](https://img.shields.io/badge/license-BackspaceAlpha-blue.svg)](./LICENSE)
[![PyPI](https://img.shields.io/pypi/v/backspaceAlpha.svg)](https://pypi.org/project/backspaceAlpha/)

A simple, customisable, easy-to-use backtesting framework with example strategies to quickly and effectively track a strategies' impact and improve it

### Contents:
1. [Overview](#1-overview)
2. [Installation](#2-installation)
3. [Usage](#3-usage)
4. [Documentation](#4-documentation)
    1. [Framework](#41---framework)
        1. [backtest.py](#411---backtestpy)
        2. [broker.py](#412---brokerpy)
        3. [loader.py](#413---loaderpy)
        4. [strategy.py](#414---strategypy)
    2. [Functions](#42---functions)
5. [Attribution](#5-attribution)



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

#### 4.1.1 - backtest.py
This module can be imported into the project using:
```python
from backspaceAlpha.framework import *
```
This script defines two main classes that are both used to run the backtest effectively. It also handles the versatile graphing functions which allow for practically any variable to be plotted and any graph to be created. It brings together all other classes.

**Imports** `MultiDataFeed`, `Broker`, `Strategy`, `matplotlib`, `numpy`, `tqdm`, `datetime`

**Classes** `BaseBackTest`, `BackTest`

---
`BaseBackTest`

The internal engine that actually runs the backtest. It handles a single strategy and only is capable of running one backtest. It simulates the whole trading environment and each tick realistically before outputting logs.

**Constructor**

Initialises the backtest and all classes that are needed to make it run. Also intialises the strategy.
```python
BaseBackTest(strategy, time_frame, start=10000, source="YAHOO", interval="1D", verbose=False, hedging=False)
```
- `strategy` - `Strategy`: This is the strategy that the backtest will run on
- `time_frame` - `(YYYY-MM-DD, YYYY-MM-DD)`: This is the time frame on which the backtest will run on where the first element of the tuple is the start date, and the last element, the end date
- `start` - (optional) `float`: This is the amount of money the strategy will start with
- `source` - (optional) `str`: This is the source from where the data is pulled (only current working option is `YAHOO`)
- `interval` - (optional) `str`: This is how often the strategy is to be run. Can choose from `1D`, `1W` and `1M` for daily, weekly and monthly respectively
- `verbose` - (optional) `bool`: Turning this on causes the broker to log updates to console every tick. Useful for debugging strategies and shows all orders and how they were handled that tick
- `hedging` - (optional) `bool`: Turning this on causes the broker to simulate a broker which allows hedging. This means certain order conflicts are handled differently (and generally more leniently)

**run**

Heart of the backtest and run it with the basic loop: Updates data feed by 1 tick, sends new data to broker first, then sends same data to strategy, allows broker to respond to new orders from strategy
```python
run(pbar = None)
```
- `pbar` - (optional) `tqdm`: If the current backtest is part of a series of backtests that is being run on different strategies, the progress of the backtest is updated on the progress bar given in the parameter. This allows for the progress bar to show the progress of a backtest on multiple strategies more effectively

---
`BackTest`

This is the main class to be used when running any backtest. It makes use of the `BaseBackTest` class

#### 4.1.2 - broker.py
#### 4.1.3 - loader.py
#### 4.1.4 - strategy.py

### 4.2 - Functions
This section includes a certain type of script, called functions, that can be used with [graph_function](). These are used for more complex graphs that require access to the whole log.

## 5. Attribution
This software is licensed under the **[BackspaceAlpha License v1.0](https://github.com/aadideepchand25/backspaceAlpha/blob/main/LICENSE)**.  
Use of this software requires attribution
Modifications must be submitted via the official GitHub repository.