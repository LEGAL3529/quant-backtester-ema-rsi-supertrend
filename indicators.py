import pandas as pd

def calculate_ema(df, period=14):
    return df['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = df['high'].combine(df['low'], max) - df['low'].combine(df['close'], min)
    atr = atr.rolling(window=period).mean()

    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    supertrend = [0] * len(df)
    for i in range(1, len(df)):
        if df['close'][i] > upperband[i - 1]:
            supertrend[i] = lowerband[i]
        elif df['close'][i] < lowerband[i - 1]:
            supertrend[i] = upperband[i]
        else:
            supertrend[i] = supertrend[i - 1]

    return pd.Series(supertrend, index=df.index)
