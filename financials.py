import pandas as pd
import requests as req

api_key = '4GFAEI5O82MQWDKF'

url = "https://www.alphavantage.co/query?function=TIME_SERIES_Daily&symbol=MSFT&apikey="
url2 = "https://www.alphavantage.co/query?function=TIME_SERIES_Daily&symbol="

N = 5
# N = number of days from Current day


# Loop through the list of Stocks and perform a request for data on each
stock_list = []
stock_list1 = ['VIX','DJI','SPX','NDX']
for stock in stock_list1:

        response = req.get(url2 + stock + "&apikey=" + api_key).json()
        stock_list.append(response)
        #print(query_url + city)


# Find N date in relation to today
from datetime import datetime, timedelta

date_N_days_ago = datetime.now() - timedelta(days=N)

#print(datetime.now())
#print(date_N_days_ago)


# Format date string
from dateutil.parser import parse
test = str(date_N_days_ago)
dt = parse(test)
#print(dt)
# datetime.datetime(2010, 2, 15, 0, 0)
#print(dt.strftime('%Y-%m-%d'))
# 15/02/2010



Vix_df = pd.DataFrame(stock_list[0]['Time Series (Daily)'])
SPX_DF = pd.DataFrame(stock_list[2]['Time Series (Daily)'])
DJI_DF = pd.DataFrame(stock_list[1]['Time Series (Daily)'])
NDX_DF = pd.DataFrame(stock_list[3]['Time Series (Daily)'])

SPX_trans = SPX_DF.transpose()
DJI_trans = DJI_DF.transpose()
NDX_trans = NDX_DF.transpose()

spxtest = pd.DataFrame(SPX_trans.reset_index(drop=False))
djitest = pd.DataFrame(DJI_trans.reset_index(drop=False))
ndxtest = pd.DataFrame(NDX_trans.reset_index(drop=False))

spxtest['new_date'] =  pd.to_datetime(spxtest['index'], format='%Y%m%d', errors='ignore')
djitest['new_date'] =  pd.to_datetime(djitest['index'], format='%Y%m%d', errors='ignore')
ndxtest['new_date'] =  pd.to_datetime(ndxtest['index'], format='%Y%m%d', errors='ignore')


#max_df.filter['new_date'] > '2018-02-012'
spx_filtered = spxtest.new_date >= '2018-02-12'
dji_filtered = djitest.new_date >= '2018-02-12'
ndx_filtered = ndxtest.new_date >= '2018-02-12'

dji =  djitest[dji_filtered]
spx =  spxtest[spx_filtered]
ndx =  ndxtest[ndx_filtered]

ndx = ndx.filter(['new_date','5. volume','4. close'])
spx = spx.filter(['new_date','5. volume','4. close'])
dji = dji.filter(['new_date','5. volume','4. close'])

Vix_trans = Vix_df.transpose()

#Vix_trans.head()


Vix_trans['Open'] = Vix_trans['1. open'].astype(float)
Vix_trans['Close'] = Vix_trans['4. close'].astype(float)


Vix_trans['AVG'] = (Vix_trans['Open'] + Vix_trans['Close']) / 2

Vix = Vix_trans['AVG'].max()

vixtest = pd.DataFrame(Vix_trans.reset_index(drop=False))

#df.rename(columns={'index': 'Date'}, inplace=True)
#vixtest.head()

vix_max = vixtest.sort_values(by='AVG', ascending=False)

vix_max['new_date'] =  pd.to_datetime(vix_max['index'], format='%Y%m%d', errors='ignore')

#vix_max.head()

#max_df.filter['new_date'] > '2018-02-012'
df_filtered = vix_max.new_date >= '2018-02-12'

vix =  vix_max[df_filtered]
vix.sort_values(by='AVG', ascending=False)
vix1 = vix.set_index('new_date')

Max_Vix_Date = vix1.iloc[0,0]
#Max_Vix_Date


#Final output for Anselmo's code: Dataframes: spx, dji, ndx
#Final output for Anselmo's code: variable: Max_Vix_Date

path = "Financials/"

spx = spx.rename(columns = {'new_date': 'Date',
                            '5. volume': 'SPX Volume',
                            '4. close': 'SPX Price'}).set_index('Date')

spx.to_csv(path + "spx.csv", float_format = '%.2g')

dji = dji.rename(columns = {'new_date': 'Date',
                            '5. volume': 'DJI Volume',
                            '4. close': 'DJI Price'}).set_index('Date')
dji.to_csv(path + "dji.csv", float_format = '%.2g')

ndx = ndx.rename(columns = {'new_date': 'Date',
                            '5. volume': 'NDX Volume',
                            '4. close': 'NDX Price'}).set_index('Date')
ndx.to_csv(path + "ndx.csv", float_format = '%.2g')