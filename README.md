git clone https://github.com/foozy74/Bitcoinbot.git
cd Bitcoinbot
```

2. Set up your development environment:
```bash
python setup_local.py
```
This script will:
- Check Python version compatibility
- Generate requirements.txt file
- Install required dependencies
- Create local environment configuration

3. Start the application:
```bash
streamlit run trading_bot.py
```

## AWS Deployment

1. Make sure you have AWS CLI installed and configured:
```bash
aws configure
```

2. Deploy to AWS Elastic Beanstalk:
```bash
cd Bitcoinbot  # Make sure you're in the project root directory
python cloudformation/deploy.py --stack-name bitcoin-bot-stack --db-password your-secure-password
```

Note: Run the deploy command from the project root directory, not from inside the cloudformation folder.

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