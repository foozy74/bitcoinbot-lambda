import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import ccxt
from strategy import MovingAverageCrossover
from utils import calculate_metrics, format_number
from database import get_db, save_trade, save_performance, save_settings
from config import APP_CONFIG, TRADING_CONFIG

# Page config
st.set_page_config(page_title="Bitcoin Trading Bot", layout="wide")
st.title("Bitcoin Trading Bot")

# Initialize database session
db = next(get_db())

# Sidebar
st.sidebar.header("Trading Parameters")
timeframe = st.sidebar.selectbox(
    "Timeframe",
    options=["1h", "4h", "1d"],
    index=2
)

lookback_period = st.sidebar.slider(
    "Lookback Period (days)",
    min_value=30,
    max_value=365,
    value=TRADING_CONFIG['default_lookback']
)

initial_balance = st.sidebar.number_input(
    "Initial Balance (USD)",
    min_value=1000,
    max_value=1000000,
    value=TRADING_CONFIG['default_initial_balance']
)

# Strategy parameters
short_window = st.sidebar.slider("Short MA Window", 5, 50, 20)
long_window = st.sidebar.slider("Long MA Window", 20, 200, 50)

# Save settings to database
settings = {
    'short_window': short_window,
    'long_window': long_window,
    'initial_balance': initial_balance,
    'timeframe': timeframe,
    'lookback_period': lookback_period
}
save_settings(db, settings)

# Fetch data
@st.cache_data(ttl=3600)
def fetch_bitcoin_data(timeframe, lookback_days):
    try:
        # Initialize Kraken exchange
        exchange = ccxt.kraken({
            'enableRateLimit': True,
        })

        # Calculate time parameters
        end_time = exchange.milliseconds()
        start_time = end_time - (lookback_days * 24 * 60 * 60 * 1000)

        # Fetch OHLCV data
        ohlcv = exchange.fetch_ohlcv(
            symbol='BTC/USD',  # Kraken uses USD instead of USDT
            timeframe=timeframe,
            since=start_time,
            limit=1000
        )

        # Convert to DataFrame
        df = pd.DataFrame(
            ohlcv,
            columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
        )
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        return df
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

try:
    with st.spinner('Fetching Bitcoin data...'):
        data = fetch_bitcoin_data(timeframe, lookback_period)

    if data is not None:
        # Initialize strategy
        strategy = MovingAverageCrossover(
            short_window=short_window,
            long_window=long_window,
            initial_balance=initial_balance
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

        # Display charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Price and Signals")
            fig = go.Figure()

            # Candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'],
                    name="OHLC"
                )
            )

            # Moving averages
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=signals['SMA_short'],
                    name=f"SMA {short_window}",
                    line=dict(color='blue')
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=signals['SMA_long'],
                    name=f"SMA {long_window}",
                    line=dict(color='orange')
                )
            )

            # Buy/Sell signals
            buy_signals = signals[signals['signal'] == 1]
            sell_signals = signals[signals['signal'] == -1]

            fig.add_trace(
                go.Scatter(
                    x=buy_signals.index,
                    y=buy_signals['close'],
                    mode='markers',
                    name='Buy Signal',
                    marker=dict(symbol='triangle-up', size=15, color='green')
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=sell_signals.index,
                    y=sell_signals['close'],
                    mode='markers',
                    name='Sell Signal',
                    marker=dict(symbol='triangle-down', size=15, color='red')
                )
            )

            fig.update_layout(
                title="Bitcoin Price and Trading Signals",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Portfolio Performance")
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=portfolio_value.index,
                    y=portfolio_value['portfolio_value'],
                    name="Portfolio Value",
                    line=dict(color='green')
                )
            )

            fig.update_layout(
                title="Portfolio Value Over Time",
                xaxis_title="Date",
                yaxis_title="Value (USD)",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

        # Performance metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Return", f"{metrics['total_return']:.2f}%")
        with col2:
            st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
        with col3:
            st.metric("Max Drawdown", f"{metrics['max_drawdown']:.2f}%")
        with col4:
            st.metric("Win Rate", f"{metrics['win_rate']:.2f}%")

        # Trade history
        st.subheader("Trade History")
        st.dataframe(trades)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")