import pandas as pd
import os

target_path = "Sentiment_Analyzer/"

target_csv_list = [target_path + "@WSJ.csv",
                   target_path + "@FT.csv", 
                   target_path + "@nyTimes.csv", 
                   target_path + "@barronsonline.csv", 
                   target_path + "@IBDinvestors.csv",
                   target_path + "@CNN.csv", 
                   target_path + "@wired.csv", 
                   target_path + "@business.csv", 
                   target_path + "@USAToday.csv", 
                   target_path + "@FoxBusiness.csv"]




#read in the csvfiles
for csv_item in target_csv_list:
    
    #read in the Indices data/reset values in the for loop
    spx_path = os.path.join('Financials/spx.csv')
    spx_df = pd.read_csv(spx_path)
    spx_df['Date'] = pd.to_datetime(spx_df['Date'])
    spx_df['SPX Price'] = spx_df['SPX Price'].map('{:.2f}'.format)

    dji_path = os.path.join('Financials/dji.csv')
    dji_df = pd.read_csv(dji_path)
    dji_df['Date'] = pd.to_datetime(dji_df['Date'])
    dji_df['DJI Price'] = dji_df['DJI Price'].map('{:.2f}'.format)

    ndx_path = os.path.join('Financials/ndx.csv')
    ndx_df = pd.read_csv(ndx_path)
    ndx_df['Date'] = pd.to_datetime(ndx_df['Date'])
    ndx_df['NDX Price'] = ndx_df['NDX Price'].map('{:.2f}'.format)

    all_df = ""
        
    #create df for each file
    df = pd.read_csv(csv_item)
    df['Date'] = pd.to_datetime(df['Date'])
    df['TextBlob'] = df['TextBlob'].map('{:.3f}'.format)
    df['Vader'] = df['Vader'].map('{:.3f}'.format)

    
    
    #since the df is sorted by days, we can call the last 30 rows for the last 30 days and reassign df
    df = df.tail(30)
    
    #Merges
    #SP500
    spx_df = pd.merge(df,spx_df, how='outer', on='Date').reset_index(drop=True).fillna(0).sort_values(by='Date')        
    spx_df = spx_df.reset_index(drop=True)
    #spx_df.to_csv(csv_item[:-4] + "_spx.csv")
        
    #Dow Jones
    dji_df = pd.merge(spx_df,dji_df, how='outer', on='Date').reset_index(drop=True).fillna(0).sort_values(by='Date')
    dji_df = dji_df.reset_index(drop=True)
    #dji_df.to_csv(csv_item[:-4] + "_dji.csv")
        
    #NASDAQ - 
    ndx_df = pd.merge(dji_df,ndx_df, how='outer', on='Date').reset_index(drop=True).fillna(0).sort_values(by='Date')
        
    #final merge to combine all data
    all_df = ndx_df.reset_index(drop=True)
        
    end_path = "Merged/"
        
    all_df.to_csv(end_path + csv_item[19:-4] + "_all.csv")
        
        