def getMA(df, maperiod ,ema):
    
    if ema == True:
        # Use exponential moving average
        ma = df['close'].ewm(com = maperiod - 1, adjust=True, min_periods = maperiod).mean()
        
    else:
        # Use simple moving average
        ma = df['close'].rolling(window = maperiod).mean()
        
    return ma