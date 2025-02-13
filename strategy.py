import pandas as pd
import numpy as np

class MovingAverageCrossover:
    def __init__(self, short_window, long_window, initial_balance):
        self.short_window = short_window
        self.long_window = long_window
        self.initial_balance = float(initial_balance)

    def generate_signals(self, data):
        signals = data.copy()

        # Calculate moving averages
        signals['SMA_short'] = signals['close'].rolling(window=self.short_window).mean()
        signals['SMA_long'] = signals['close'].rolling(window=self.long_window).mean()

        # Generate trading signals
        signals['signal'] = 0
        # Create a mask for valid entries (after both MAs are available)
        valid_entries = signals.index >= signals.index[self.long_window - 1]
        # Use boolean indexing with the mask
        signals.loc[valid_entries, 'signal'] = np.where(
            signals.loc[valid_entries, 'SMA_short'] > signals.loc[valid_entries, 'SMA_long'],
            1,
            0
        )

        # Generate trading orders
        signals['position'] = signals['signal'].diff()

        return signals

    def backtest(self, data):
        signals = self.generate_signals(data)
        portfolio = pd.DataFrame(index=signals.index)

        # Initialize portfolio metrics with explicit data types
        portfolio['position'] = signals['position'].astype(float)
        portfolio['close'] = signals['close'].astype(float)
        portfolio['cash'] = pd.Series(self.initial_balance, index=portfolio.index, dtype=float)
        portfolio['holdings'] = pd.Series(0.0, index=portfolio.index, dtype=float)
        portfolio['portfolio_value'] = pd.Series(self.initial_balance, index=portfolio.index, dtype=float)

        # Initialize trade history
        trades = []

        position = 0
        entry_price = 0

        for i in range(len(portfolio)):
            current_time = portfolio.index[i]
            if portfolio['position'].iloc[i] == 1:  # Buy signal
                entry_price = portfolio['close'].iloc[i]
                btc_amount = portfolio['cash'].iloc[i] / entry_price
                portfolio.loc[portfolio.index[i:], 'holdings'] = float(btc_amount)
                portfolio.loc[portfolio.index[i:], 'cash'] = 0.0
                position = 1

                trades.append({
                    'timestamp': current_time,
                    'type': 'BUY',
                    'price': float(entry_price),
                    'amount': float(btc_amount),
                    'value': float(btc_amount * entry_price)
                })

            elif portfolio['position'].iloc[i] == -1 and position == 1:  # Sell signal
                exit_price = portfolio['close'].iloc[i]
                btc_amount = portfolio['holdings'].iloc[i]
                cash_value = float(btc_amount * exit_price)
                portfolio.loc[portfolio.index[i:], 'cash'] = cash_value
                portfolio.loc[portfolio.index[i:], 'holdings'] = 0.0
                position = 0

                trades.append({
                    'timestamp': current_time,
                    'type': 'SELL',
                    'price': float(exit_price),
                    'amount': float(btc_amount),
                    'value': float(cash_value)
                })

            # Update portfolio value with explicit float casting
            portfolio.loc[portfolio.index[i], 'portfolio_value'] = float(
                portfolio['cash'].iloc[i] +
                portfolio['holdings'].iloc[i] * portfolio['close'].iloc[i]
            )

        trades_df = pd.DataFrame(trades)
        if not trades_df.empty:
            trades_df.set_index('timestamp', inplace=True)

        return signals, portfolio, trades_df