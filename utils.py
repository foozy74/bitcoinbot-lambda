import numpy as np
import pandas as pd

def calculate_metrics(portfolio, trades):
    """Calculate trading performance metrics"""
    metrics = {}
    
    # Total Return
    initial_value = portfolio['portfolio_value'].iloc[0]
    final_value = portfolio['portfolio_value'].iloc[-1]
    metrics['total_return'] = ((final_value - initial_value) / initial_value) * 100
    
    # Daily returns
    portfolio['daily_returns'] = portfolio['portfolio_value'].pct_change()
    
    # Sharpe Ratio (assuming risk-free rate of 0.01)
    risk_free_rate = 0.01
    excess_returns = portfolio['daily_returns'] - risk_free_rate/252
    metrics['sharpe_ratio'] = np.sqrt(252) * excess_returns.mean() / excess_returns.std()
    
    # Maximum Drawdown
    portfolio['cummax'] = portfolio['portfolio_value'].cummax()
    portfolio['drawdown'] = (portfolio['portfolio_value'] - portfolio['cummax']) / portfolio['cummax']
    metrics['max_drawdown'] = portfolio['drawdown'].min() * 100
    
    # Win Rate
    if not trades.empty:
        trades['return'] = 0.0
        for i in range(0, len(trades), 2):
            if i + 1 < len(trades):
                entry = trades.iloc[i]
                exit = trades.iloc[i + 1]
                trade_return = (exit['price'] - entry['price']) / entry['price']
                trades.iloc[i:i+2, trades.columns.get_loc('return')] = trade_return
        
        winning_trades = len(trades[trades['return'] > 0]) / 2
        total_trades = len(trades) / 2
        metrics['win_rate'] = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    else:
        metrics['win_rate'] = 0
    
    return metrics

def format_number(num):
    """Format numbers for display"""
    if abs(num) >= 1e6:
        return f"{num/1e6:.2f}M"
    elif abs(num) >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"
