import os
from dotenv import load_dotenv

# Load environment variables from .env file in development
if os.getenv('AWS_EXECUTION_ENV') is None:
    load_dotenv()

# Database configuration
DATABASE_CONFIG = {
    'host': os.getenv('PGHOST'),
    'port': os.getenv('PGPORT'),
    'user': os.getenv('PGUSER'),
    'password': os.getenv('PGPASSWORD'),
    'database': os.getenv('PGDATABASE'),
}

# Application configuration
APP_CONFIG = {
    'debug': os.getenv('DEBUG', 'False').lower() == 'true',
    'host': '0.0.0.0',
    'port': int(os.getenv('PORT', 5000))
}

# Trading configuration
TRADING_CONFIG = {
    'default_timeframe': '1d',
    'default_lookback': 100,
    'default_initial_balance': 10000
}
