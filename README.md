# Bitcoin Trading Bot

A sophisticated Bitcoin trading bot that provides advanced mock trading functionality and strategy backtesting with robust data handling and interactive visualizations.

## Features

- Real-time Bitcoin price monitoring
- Moving Average Crossover strategy implementation
- Interactive Streamlit dashboard
- Performance metrics and visualization
- AWS deployment support
- Database integration for trade logging

## Getting Started

### Prerequisites

- Python 3.11 or later
- PostgreSQL database
- AWS account (for cloud deployment)

### Installation

1. Clone the repository:
```bash
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
```

2. Access the dashboard at `http://localhost:5000`

## AWS Deployment

Refer to `aws_deployment.md` for detailed AWS deployment instructions using CloudFormation.

## Database Configuration

The application requires a PostgreSQL database. Set the following environment variables:
- DATABASE_URL
- PGHOST
- PGPORT
- PGUSER
- PGPASSWORD
- PGDATABASE

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
