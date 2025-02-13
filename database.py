from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Get database URL from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    type = Column(String)  # 'BUY' or 'SELL'
    price = Column(Float)
    amount = Column(Float)
    value = Column(Float)

class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, unique=True, index=True)
    portfolio_value = Column(Float)
    daily_return = Column(Float)
    total_return = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    short_window = Column(Integer)
    long_window = Column(Integer)
    initial_balance = Column(Float)
    timeframe = Column(String)
    lookback_period = Column(Integer)

# Create all tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_trade(db, trade_data):
    """Save trade to database"""
    # Convert pandas Timestamp to datetime if necessary
    timestamp = trade_data.get('timestamp', datetime.utcnow())
    if hasattr(timestamp, 'to_pydatetime'):
        timestamp = timestamp.to_pydatetime()

    trade = Trade(
        timestamp=timestamp,
        type=trade_data['type'],
        price=float(trade_data['price']),
        amount=float(trade_data['amount']),
        value=float(trade_data['value'])
    )
    db.add(trade)
    db.commit()
    return trade

def save_performance(db, metrics, date):
    """Save daily performance metrics"""
    # Convert pandas Timestamp to datetime if necessary
    if hasattr(date, 'to_pydatetime'):
        date = date.to_pydatetime()

    performance = Performance(
        date=date,
        portfolio_value=float(metrics['portfolio_value']),
        daily_return=float(metrics.get('daily_return', 0)),
        total_return=float(metrics['total_return']),
        sharpe_ratio=float(metrics['sharpe_ratio']),
        max_drawdown=float(metrics['max_drawdown'])
    )
    db.add(performance)
    db.commit()
    return performance

def save_settings(db, settings):
    """Save trading settings"""
    setting = Settings(
        short_window=settings['short_window'],
        long_window=settings['long_window'],
        initial_balance=float(settings['initial_balance']),
        timeframe=settings['timeframe'],
        lookback_period=settings['lookback_period']
    )
    db.add(setting)
    db.commit()
    return setting