git clone https://github.com/foozy74/Bitcoinbot.git
cd Bitcoinbot
```

2. Set up your development environment:
```bash
python setup_local.py
```
This script will:
- Check Python version compatibility
- Install required dependencies
- Create local environment configuration

3. Start the application:
```bash
streamlit run trading_bot.py
```

## Features
- Real-time Bitcoin price monitoring
- Moving Average Crossover strategy implementation
- Interactive backtesting with customizable parameters
- Performance metrics visualization
- Trade history tracking
- PostgreSQL database integration for trade logging

## Required Packages
- streamlit: Web application framework
- pandas: Data manipulation and analysis
- numpy: Numerical computing
- plotly: Interactive visualizations
- python-dotenv: Environment variable management
- boto3: AWS SDK for Python
- ccxt: Cryptocurrency exchange API
- sqlalchemy: Database ORM
- psycopg2-binary: PostgreSQL adapter

## Repository Synchronization

To sync your local repository with the latest changes:

```bash
python sync_repo.py
```

Options:
- `--repo`: Specify a different repository URL
- `--branch`: Specify a different branch (default: main)

Example:
```bash
python sync_repo.py --branch development