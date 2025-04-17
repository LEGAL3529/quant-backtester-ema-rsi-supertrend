
import pandas as pd

def calculate_ema(df, period=14):
    return df['close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(df, period=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = df['high'].combine(df['low'], max) - df['low'].combine(df['high'], min)
    atr = atr.rolling(window=period).mean()
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)
    supertrend = [True] * len(df)
    
    for i in range(1, len(df)):
        if df['close'][i] > upperband[i - 1]:
            supertrend[i] = True
        elif df['close'][i] < lowerband[i - 1]:
            supertrend[i] = False
        else:
            supertrend[i] = supertrend[i - 1]
    return supertrend

def apply_strategy(df):
    df['ema'] = calculate_ema(df)
    df['rsi'] = calculate_rsi(df)
    df['supertrend'] = calculate_supertrend(df)

    last = df.iloc[-1]
    if last['supertrend'] and last['rsi'] < 30 and last['close'] > last['ema']:
        return 'BUY'
    elif not last['supertrend'] and last['rsi'] > 70 and last['close'] < last['ema']:
        return 'SELL'
    else:
        return 'HOLD'

def generate_signal(df):
    return apply_strategy(df)
