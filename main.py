import loader
import matplotlib.pyplot as plt
import pandas as pd
data_csv = loader.loader('data')

data_csv.ticker.dropna(how='any')
data_csv.trader.dropna(how='any')
# data_csv.ticker.plot(kind='line',x = 'exchange_ts',y='bpx',figsize=(10,6))

# 
# print(data_csv.trader['Price'])
# print((data_csv.trader['Price'] == 0).any())
# print(data_csv.ticker.loc[0])
# print(data_csv.trader.loc[0])
data_csv.ticker = data_csv.ticker[data_csv.ticker['exchange_ts'] != 0]
data_csv.ticker = data_csv.ticker[data_csv.ticker['bpx'] != 0]
data_csv.ticker = data_csv.ticker[data_csv.ticker['bqty'] != 0]
data_csv.ticker = data_csv.ticker[data_csv.ticker['apx'] != 0]
data_csv.ticker = data_csv.ticker[data_csv.ticker['aqty'] != 0]
data_csv.trader = data_csv.trader[data_csv.trader['exchange_ts']!=0]
data_csv.trader = data_csv.trader[data_csv.trader['Price']!=0]
data_csv.trader = data_csv.trader[data_csv.trader['Qty']!=0]




data_csv.ticker['exchange_ts'] = pd.to_datetime(data_csv.ticker['exchange_ts'],unit='s',utc=True)
data_csv.trader['exchange_ts'] = pd.to_datetime(data_csv.trader['exchange_ts'],unit='s',utc=True)
data_csv.ticker.set_index('exchange_ts',inplace=True)
data_csv.ticker.index = pd.to_datetime(data_csv.ticker.index)
ticker = data_csv.ticker.resample('S').last()
ticker.fillna(0,inplace=True)
ticker['bpx'][0] = 0
ticker['apx'][0] = 0
ticker['aqty'][0] = 0
ticker['bqty'][0] = 0
# data_csv.trader.set_index('exchange_ts',inplace=True)
# print(data_csv.colum_ticker)
print(ticker)
# print(data_csv.colum_trader)
# print(data_csv.trader)
# data_csv.ticker.plot(kind='line',x = 'exchange_ts',y='bpx',figsize=(10,6))
# data_csv.trader.plot(kind='line',x = 'exchange_ts',y='Price',figsize=(10,6))
# plt.show()
trader_all = pd.DataFrame(columns=['totaltrade', 'Qty', 'exchange_ts'])
# trader_sell = pd.DataFrame(columns=['totalsell', 'average_price', 'Qty', 'exchange_ts'])
# trader_buy = pd.DataFrame(columns=['totalbuy', 'average_price', 'Qty', 'exchange_ts'])

trader_all['totaltrade'] = data_csv.trader['Price']*data_csv.trader['Qty']
trader_all['Qty'] = data_csv.trader['Qty']
trader_all['exchange_ts'] = data_csv.trader['exchange_ts']
trader_all['m'] = data_csv.trader['m']
# print(trader_all)

trader_sell = trader_all[trader_all['m'] == True]
trader_buy = trader_all[trader_all['m'] == False]
# print(trader_buy)

# The average price in every second (buy and sell)

trader_sell.set_index('exchange_ts',inplace=True)
trader_sell.index = pd.to_datetime(trader_sell.index)
trader_sell = trader_sell.resample('S').sum()
trader_sell['average_price'] = trader_sell['totaltrade'] / trader_sell['Qty']
trader_sell.fillna(0,inplace=True)
trader_sell['m'] = True


trader_buy.set_index('exchange_ts',inplace=True)
trader_buy.index = pd.to_datetime(trader_buy.index)
trader_buy = trader_buy.resample('S').sum()
trader_buy['average_price'] = trader_buy['totaltrade'] / trader_buy['Qty']
trader_buy.fillna(0,inplace=True)
trader_buy['m'] = False
# print(trader_sell)
# print(trader_buy)


# the trader volum and 
trader_data = pd.DataFrame(columns=['volum_dollor', 'sub_dollor', 'volum_btc', 'sub_btc'])
# trader_data['exchange_ts'] = trader_buy['exchange_ts']
# trader_data.set_index('exchange_ts',inplace=True)
# trader_data.index = pd.to_datetime(trader_data.index)
trader_data['volum_dollor'] = trader_buy['totaltrade'] + trader_sell['totaltrade']
trader_data['sub_dollor'] = trader_buy['totaltrade'] - trader_sell['totaltrade']
trader_data['sub_volum_dollor'] = trader_data['sub_dollor'] / trader_data['volum_dollor'] # OFI_trader
trader_data['volum_btc'] = trader_buy['Qty'] + trader_sell['Qty']
trader_data['sub_btc'] = trader_buy['Qty'] - trader_sell['Qty']
trader_data['sub_volum_btc'] = trader_data['sub_btc'] / trader_data['volum_btc']
trader_data['average_price'] = (ticker['bpx'] + ticker['apx']) / 2
trader_data['maker_pricesub'] = ticker['apx'] - ticker['bpx']
trader_data['maker_price_sub_avg'] = trader_data['maker_pricesub'] / trader_data['average_price']

trader_data['maker_btcsub'] = ticker['aqty'] - ticker['bqty']
trader_data['maker_btcimbalance'] = trader_data['maker_btcsub'] / (ticker['aqty'] + ticker['bqty'])
trader_data['volum_ma60'] = trader_data['volum_dollor'].rolling(60).mean()
trader_data['price_ma60'] = trader_data['average_price'].rolling(60).mean()
# trader_data.loc[0] = 0

trader_data['diff_buy'] = ticker['bpx'].diff()
trader_data['diff_sell'] = ticker['apx'].diff()
# trader_data['OFI_buy'] = (trader_data['diff_buy'] > 0) * ticker['bqty'] + (trader_data['diff_buy'] < 0) * (-ticker['bqty']) + (trader_data['diff_buy'] == 0) * ()

trader_data.fillna(0,inplace=True)





print(trader_data)
# 

# trader_sub = trader_sell - trader_buy
# trader_sub.fillna(0,inplace=True)

# print(trader_sub

# pricise
furture_3 = pd.DataFrame(columns=['price_3','pecent_3'])
furture_5 = pd.DataFrame(columns=['price_5','pecent_5'])
furture_10 = pd.DataFrame(columns=['price_10','pecent_10'])

furture_3['price_3'] = trader_data['average_price'].shift(-3)
furture_3['pecent_3'] = (furture_3['price_3'] - trader_data['average_price']) / trader_data['average_price']

furture_5['price_5'] = trader_data['average_price'].shift(-5)
furture_5['pecent_5'] = (furture_3['price_5'] - trader_data['average_price']) / trader_data['average_price']

furture_10['price_10'] = trader_data['average_price'].shift(-10)
furture_10['pecent_10'] = (furture_3['price_10'] - trader_data['average_price']) / trader_data['average_price']


# print(furture_3)
# print(furture_5)
# print(furture_10)
