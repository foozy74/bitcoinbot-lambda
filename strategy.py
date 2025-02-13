import pandas as pd
import numpy as np

class MovingAverageCrossover:
    def __init__(self, short_window, long_window, initial_balance):
        self.short_window = short_window
        self.long_window = long_window
        self.initial_balance = initial_balance
    
    def generate_signals(self, data):
        signals = data.copy()
        
        # Calculate moving averages
        signals['SMA_short'] = signals['close'].rolling(window=self.short_window).mean()
        signals['SMA_long'] = signals['close'].rolling(window=self.long_window).mean()
        
        # Generate trading signals
        signals['signal'] = 0
        signals['signal'][self.long_window:] = np.where(
            signals['SMA_short'][self.long_window:] > signals['SMA_long'][self.long_window:],
            1,
            0
        )
        
        # Generate trading orders
        signals['position'] = signals['signal'].diff()
        
        return signals
    
    def backtest(self, data):
        signals = self.generate_signals(data)
        portfolio = pd.DataFrame(index=signals.index)
        
        # Initialize portfolio metrics
        portfolio['position'] = signals['position']
        portfolio['close'] = signals['close']
        portfolio['cash'] = self.initial_balance
        portfolio['holdings'] = 0
        portfolio['portfolio_value'] = self.initial_balance
        
        # Initialize trade history
        trades = []
        
        position = 0
        entry_price = 0
        
        for i in range(len(portfolio)):
            if portfolio['position'].iloc[i] == 1:  # Buy signal
                entry_price = portfolio['close'].iloc[i]
                btc_amount = portfolio['cash'].iloc[i] / entry_price
                portfolio.loc[portfolio.index[i:], 'holdings'] = btc_amount
                portfolio.loc[portfolio.index[i:], 'cash'] = 0
                position = 1
                
                trades.append({
                    'date': portfolio.index[i],
                    'type': 'BUY',
                    'price': entry_price,
                    'amount': btc_amount,
                    'value': btc_amount * entry_price
                })
                
            elif portfolio['position'].iloc[i] == -1 and position == 1:  # Sell signal
                exit_price = portfolio['close'].iloc[i]
                btc_amount = portfolio['holdings'].iloc[i]
                cash_value = btc_amount * exit_price
                portfolio.loc[portfolio.index[i:], 'cash'] = cash_value
                portfolio.loc[portfolio.index[i:], 'holdings'] = 0
                position = 0
                
                trades.append({
                    'date': portfolio.index[i],
                    'type': 'SELL',
                    'price': exit_price,
                    'amount': btc_amount,
                    'value': cash_value
                })
            
            # Update portfolio value
            portfolio.loc[portfolio.index[i], 'portfolio_value'] = (
                portfolio['cash'].iloc[i] +
                portfolio['holdings'].iloc[i] * portfolio['close'].iloc[i]
            )
        
        trades_df = pd.DataFrame(trades)
        if not trades_df.empty:
            trades_df.set_index('date', inplace=True)
        
        return signals, portfolio, trades_df
