import json
import os
import ccxt
import pandas as pd
from datetime import datetime, timedelta
from strategy import MovingAverageCrossover
from utils import calculate_metrics
from database import get_db, save_trade, save_performance

def get_trading_parameters():
    """Get trading parameters from environment variables"""
    return {
        'timeframe': os.getenv('TRADING_TIMEFRAME', '1d'),
        'lookback_period': int(os.getenv('LOOKBACK_PERIOD', '100')),
        'initial_balance': float(os.getenv('INITIAL_BALANCE', '10000')),
        'short_window': int(os.getenv('SHORT_WINDOW', '20')),
        'long_window': int(os.getenv('LONG_WINDOW', '50'))
    }

def fetch_bitcoin_data(timeframe, lookback_days):
    """Fetch Bitcoin price data from Kraken"""
    try:
        exchange = ccxt.kraken({'enableRateLimit': True})
        end_time = exchange.milliseconds()
        start_time = end_time - (lookback_days * 24 * 60 * 60 * 1000)
        
        ohlcv = exchange.fetch_ohlcv(
            symbol='BTC/USD',
            timeframe=timeframe,
            since=start_time,
            limit=1000
        )
        
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        
        return df
    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        raise

def lambda_handler(event, context):
    """AWS Lambda handler function"""
    try:
        # Get trading parameters
        params = get_trading_parameters()
        
        # Initialize database session
        db = next(get_db())
        
        # Fetch Bitcoin data
        data = fetch_bitcoin_data(params['timeframe'], params['lookback_period'])
        
        if data is not None:
            # Initialize strategy
            strategy = MovingAverageCrossover(
                short_window=params['short_window'],
                long_window=params['long_window'],
                initial_balance=params['initial_balance']
            )
            
            # Run backtest
            signals, portfolio_value, trades = strategy.backtest(data)
            
            # Save trades to database
            for _, trade in trades.iterrows():
                save_trade(db, trade.to_dict())
            
            # Calculate and save performance metrics
            metrics = calculate_metrics(portfolio_value, trades)
            metrics['portfolio_value'] = portfolio_value['portfolio_value'].iloc[-1]
            save_performance(db, metrics, datetime.now())
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Trading analysis completed successfully',
                    'metrics': {
                        'total_return': f"{metrics['total_return']:.2f}%",
                        'sharpe_ratio': f"{metrics['sharpe_ratio']:.2f}",
                        'max_drawdown': f"{metrics['max_drawdown']:.2f}%",
                        'win_rate': f"{metrics['win_rate']:.2f}%"
                    }
                })
            }
        
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Failed to fetch Bitcoin data'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
