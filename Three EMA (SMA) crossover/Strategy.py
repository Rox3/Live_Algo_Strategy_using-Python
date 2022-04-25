# KiteTicker for Current data and KiteConnect for Historical data 

from kiteconnect import KiteTicker,KiteConnect
import pandas as pd
import numpy as np
from ma import getMA



from datetime import datetime,timedelta

if __name__=='__main__':
    api_key=open('api_key.txt','r').read()
    api_secret=open('api_secret.txt','r').read()

    
    kite=KiteConnect(api_key=api_key)

### 1 if u have already written access token, access token is having 24 hr life span
    access_token=open('access_token.txt','r').read()

    kite.set_access_token(access_token)



### 2if u are opening the access data for the first time in the day 

    # print(kite.login_url())
    # ### data =kite.generate_session("REQUEST TOKEN <<5 min life span>>",api_secret=api_secret)
    # data =kite.generate_session("kxYyW3v37VMKajpM8VasoNjwKjaxh4fP",api_secret=api_secret)
    # print(data['access_token'])
    # kite.set_access_token(data['access_token'])


    # with open('access_token.txt','w') as ak:
    #     ak.write(data['access_token'])

    

    ##Dates 

    from_date=datetime.strftime(datetime.now()-timedelta(10),'%Y-%m-%d')
    to_date=datetime.today().strftime('%Y-%m-%d')

    #interval

    interval='5minute'

    tokens={
        738561:'RELIANCE',
        341249:'HDFCBANK',
        884737:'TATAMOTORS',
        81153:'BAJFINANCE',
        2714625:'BHARTIARTL' 
        #3899905:'AMBIKCO'
    }

    while True:

        ### fetch the historical data only after closing the candle
        if(datetime.now().second==0) and (datetime.now().minute%5==0):

            for token in tokens:
                records=kite.historical_data(token,from_date=from_date,to_date=to_date,interval=interval)
                print(records)
                df=pd.DataFrame(records)

                df.drop(df.tail(1).index,inplace=True)
                print(df)
                open=df['open'].values
                high=df['high'].values
                low=df['low'].values
                close=df['close'].values

                df['ma_slow']=getMA(df,13,1)
                df['ma_mid']=getMA(df,8,1)
                df['ma_fast']=getMA(df,5,1)
                print(df)
                print(df['ma_slow'].iloc[-2])
                print(df['ma_mid'].iloc[-1])
                print(df['ma_fast'].iloc[-1])
                price=kite.ltp('NSE:'+tokens[token])
                ltp=price['NSE:'+tokens[token]]['last_price']

                longFlag=False
                shortFlag=False
                profit=0

                print(ltp)

                # if (df['ma_fast'].iloc[-1]>df['ma_mid'].iloc[-1]) and  (df['ma_fast'].iloc[-2]<df['ma_mid'].iloc[-2]):
                #     buy_order_id=kite.place_order(
                #         variety=kite.VARIETY_REGULAR,
                #         exchange=kite.EXCHANGE_NSE,
                #         order_type=kite.ORDER_TYPE_MARKET,
                #         tradingsymbol=tokens[token],
                #         transaction_type=kite.TRANSACTION_TYPE_BUY,
                #         quantity=25,
                #         validity=kite.VALIDITY_DAY,
                #         product=kite.PRODUCT_MIS,
                #     )
                
                # if (df['ma_fast'].iloc[-1]<df['ma_mid'].iloc[-1]) and  (df['ma_fast'].iloc[-2]>df['ma_mid'].iloc[-2]):
                #     sell_order_id=kite.place_order(
                #         variety=kite.VARIETY_REGULAR,
                #         exchange=kite.EXCHANGE_NSE,
                #         order_type=kite.ORDER_TYPE_MARKET,
                #         tradingsymbol=tokens[token],
                #         transaction_type=kite.TRANSACTION_TYPE_SELL,
                #         quantity=25,
                #         validity=kite.VALIDITY_DAY,
                #         product=kite.PRODUCT_MIS,
                #     )


        ## Going long
                #if(ma_mid[-1]>ma_slow[-1]) and (ma_fast[-1]>ma_mid[-1]) and ((ma_mid[-2]<ma_slow[-2]) or (ma_fast[-2]<ma_mid[-2])) and longFlag== False and shortFlag==False:
                if (df['ma_mid'].iloc[-1]>df['ma_slow'].iloc[-1]) and (df['ma_fast'].iloc[-1]>df['ma_mid'].iloc[-1]) and  (df['ma_mid'].iloc[-2]<df['ma_slow'].iloc[-2]) and longFlag== False and shortFlag==False:
                    buy_order_id=kite.place_order(
                        variety=kite.VARIETY_REGULAR,
                        exchange=kite.EXCHANGE_NSE,
                        order_type=kite.ORDER_TYPE_MARKET,
                        tradingsymbol=tokens[token],
                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                        quantity=25,
                        validity=kite.VALIDITY_DAY,
                        product=kite.PRODUCT_MIS,
                    #     price=ltp,
                    #     squareoff=10,
                    #     stoploss=2,
                    #     trailing_stoploss=1,
                    
                    )
                    print("New Buy")
                    longFlag=True

                #elif (ma_fast[-1]<ma_mid[-1]) and (ma_fast[-2]>ma_mid[-2]) and longFlag== True:
                elif (df['ma_fast'].iloc[-1]<df['ma_mid'].iloc[-1]) and (df['ma_fast'].iloc[-2]>df['ma_mid'].iloc[-2]) and longFlag== True:
                    sell_order_id=kite.place_order(
                        variety=kite.VARIETY_REGULAR,
                        exchange=kite.EXCHANGE_NSE,
                        order_type=kite.ORDER_TYPE_MARKET,
                        tradingsymbol=tokens[token],
                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                        quantity=25,
                        validity=kite.VALIDITY_DAY,
                        product=kite.PRODUCT_MIS,
                    #     price=ltp,
                    #     squareoff=10,
                    #     stoploss=2,
                    #     trailing_stoploss=1,
                    
                    )
                    print("close long position")
                    longFlag=False

        ### going sort

                #elif(ma_mid[-1]<ma_slow[-1]) and (ma_fast[-1]<ma_mid[-1]) and ((ma_mid[-2]>ma_slow[-2]) or (ma_fast[-2]>ma_mid[-2])) and longFlag== False and shortFlag==False:
                elif (df['ma_mid'].iloc[-1]<df['ma_slow'].iloc[-1]) and (df['ma_fast'].iloc[-1]<df['ma_mid'].iloc[-1]) and  (df['ma_mid'].iloc[-2]>df['ma_slow'].iloc[-2]) and longFlag== False and shortFlag==False:
                    sell_order_id=kite.place_order(
                        variety=kite.VARIETY_REGULAR,
                        exchange=kite.EXCHANGE_NSE,
                        order_type=kite.ORDER_TYPE_MARKET,
                        tradingsymbol=tokens[token],
                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                        quantity=25,
                        validity=kite.VALIDITY_DAY,
                        product=kite.PRODUCT_MIS,
                    #     price=ltp,
                    #     squareoff=10,
                    #     stoploss=2,
                    #     trailing_stoploss=1,
                    
                    )
                    print("New Sell")
                    shortFlag=True

                #elif (ma_fast[-1]>ma_mid[-1]) and (ma_fast[-2]<ma_mid[-2]) and shortFlag== True:
                elif (df['ma_fast'].iloc[-1]>df['ma_mid'].iloc[-1]) and (df['ma_fast'].iloc[-2]<df['ma_mid'].iloc[-2]) and shortFlag== True:
                    sell_order_id=kite.place_order(
                        variety=kite.VARIETY_REGULAR,
                        exchange=kite.EXCHANGE_NSE,
                        order_type=kite.ORDER_TYPE_MARKET,
                        tradingsymbol=tokens[token],
                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                        quantity=25,
                        validity=kite.VALIDITY_DAY,
                        product=kite.PRODUCT_MIS,
                    #     price=ltp,
                    #     squareoff=10,
                    #     stoploss=2,
                    #     trailing_stoploss=1,
                    
                    )
                    print("Close short position")
                    shortFlag=False
            
            print(kite.orders())
                

