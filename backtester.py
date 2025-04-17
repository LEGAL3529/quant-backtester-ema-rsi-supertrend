
import pandas as pd
import matplotlib.pyplot as plt
from signals import generate_signal


def backtest_strategy(file_path):
    df = pd.read_csv(file_path, parse_dates=["timestamp"])  # <-- Обязательно!

    capital = 10000  # начальный депозит
    position = 0
    entry_price = 0
    returns = []

    for i in range(len(df)):
        signal = df['signal'].iloc[i]
        price = df['close'].iloc[i]

        if signal == 'BUY' and position == 0:
            entry_price = price
            position = 1

        elif signal == 'SELL' and position == 1:
            profit = (price - entry_price) / entry_price
            returns.append(profit)
            position = 0

    df['strategy_returns'] = 0
    if returns:
        total_return = sum(returns)
        avg_return = sum(returns) / len(returns)
        win_rate = sum([1 for r in returns if r > 0]) / len(returns)
    else:
        total_return = avg_return = win_rate = 0

    print(f"🔍 Кол-во сделок: {len(returns)}")
    print(f"💰 Общая доходность: {round(total_return * 100, 2)}%")
    print(f"📈 Средняя доходность на сделку: {round(avg_return * 100, 2)}%")
    print(f"✅ Win-rate: {round(win_rate * 100, 2)}%")

    # Визуализация
    plt.figure(figsize=(14, 6))
    plt.plot(df['timestamp'], df['close'], label='Цена')
    plt.scatter(df[df['signal'] == 'BUY']['timestamp'], df[df['signal'] == 'BUY']['close'], label='BUY', marker='^', color='green')
    plt.scatter(df[df['signal'] == 'SELL']['timestamp'], df[df['signal'] == 'SELL']['close'], label='SELL', marker='v', color='red')
    plt.title('Backtest: Buy/Sell сигналы на графике')
    plt.xlabel('Время')
    plt.ylabel('Цена')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig('backtest_result.png')
    plt.show()

if __name__ == "__main__":
    backtest_strategy("sample_data_with_easy_signals.csv")
