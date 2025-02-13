git clone https://github.com/foozy74/Bitcoinbot.git
cd Bitcoinbot
```

2. Install dependencies:
The project uses Replit's package management. Required packages:
- streamlit
- pandas
- numpy
- plotly
- python-dotenv
- boto3
- ccxt
- sqlalchemy
- psycopg2-binary

### Repository Synchronization

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
```

### Running the Application

1. Start the Streamlit application:
```bash
streamlit run trading_bot.py