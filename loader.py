import pandas as pd
class loader():
    colum_ticker = 0
    law_ticker = 0
    colum_trader = 0
    law_trader = 0
    ticker = pd.DataFrame()
    trader = pd.DataFrame()
    def __init__(self, filename):
        tickerfile = filename + '/binance_swap_ticker.csv'
        traderfile = filename + '/binance_swap_trades.csv'
        self.ticker = pd.read_csv(tickerfile)
        self.trader = pd.read_csv(traderfile)
        self.colum_ticker = self.ticker.shape[1]
        self.law_ticker = self.ticker.shape[0]
        self.colum_trader = self.trader.shape[1]
        self.law_trader = self.trader.shape[0]