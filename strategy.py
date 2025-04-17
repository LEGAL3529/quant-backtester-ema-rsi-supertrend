from indicators import calculate_ema, calculate_rsi, calculate_supertrend

def apply_strategy(df):
    df['ema'] = calculate_ema(df)
    df['rsi'] = calculate_rsi(df)
    df['supertrend'] = calculate_supertrend(df)

    signals = []
    for i in range(len(df)):
        if df['rsi'][i] < 30 and df['close'][i] > df['supertrend'][i] and df['close'][i] > df['ema'][i]:
            signals.append('BUY')
        elif df['rsi'][i] > 70 and df['close'][i] < df['supertrend'][i] and df['close'][i] < df['ema'][i]:
            signals.append('SELL')
        else:
            signals.append('HOLD')

    return signals
