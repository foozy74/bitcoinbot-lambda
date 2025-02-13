2. Entwicklungsumgebung einrichten:
```bash
python setup_local.py
```
Das Script wird:
- Python Version überprüfen
- requirements.txt Datei generieren
- Benötigte Abhängigkeiten installieren
- Lokale Umgebungskonfiguration erstellen

3. Anwendung starten:
```bash
streamlit run trading_bot.py
```

## AWS Deployment
### Web Application Deployment

1. AWS CLI installieren und konfigurieren:
```bash
aws configure
```

2. Auf AWS Elastic Beanstalk deployen:
```bash
cd Bitcoinbot  # Stellen Sie sicher, dass Sie im Projektverzeichnis sind
python cloudformation/deploy.py --stack-name bitcoin-bot-stack --db-password IhrSicheresPasswort
```

Hinweis: Führen Sie den Deploy-Befehl vom Projektverzeichnis aus, nicht aus dem cloudformation Ordner.

### Lambda Function Deployment

# Bitcoin Trading Bot Lambda

Eine AWS Lambda-Implementierung des Bitcoin Trading Bots mit automatisierter Ausführung und Datenbankintegration.

## Features

- Automatisierte Bitcoin-Handelsanalyse
- Moving Average Crossover Strategie
- Tägliche Ausführung via AWS Lambda
- Performance-Metriken Speicherung in PostgreSQL
- CloudFormation Templates für Infrastructure as Code

## Installation

1. Repository klonen:
```bash
git clone https://github.com/foozy74/bitcoinbot-lambda.git
cd bitcoinbot-lambda
```

2. Abhängigkeiten installieren:
```bash
python setup_local.py
```

## AWS Deployment

1. AWS CLI installieren und konfigurieren:
```bash
aws configure
```

2. Lambda-Funktion deployen:
```bash
python deploy_lambda.py --stack-name bitcoin-bot-lambda --db-password IhrSicheresPasswort
```

## Konfiguration

Die Lambda-Funktion kann über folgende Umgebungsvariablen konfiguriert werden:

- `TRADING_TIMEFRAME`: Zeitrahmen für die Analyse (Standard: '1d')
- `LOOKBACK_PERIOD`: Anzahl der Tage für historische Daten (Standard: 100)
- `INITIAL_BALANCE`: Startkapital für Backtesting (Standard: 10000)
- `SHORT_WINDOW`: Kurzes Moving Average Fenster (Standard: 20)
- `LONG_WINDOW`: Langes Moving Average Fenster (Standard: 50)

## Entwicklung

Für lokale Entwicklung und Tests:

```bash
python setup_local.py
python lambda_handler.py
```

## Repository Synchronisation

Aktualisieren Sie Ihr lokales Repository:

```bash
python sync_repo.py
```

## Lizenz

MIT License

Für automatisierte Ausführung als Lambda-Funktion:

```bash
python deploy_lambda.py --stack-name bitcoin-bot-lambda --db-password IhrSicheresPasswort
```

Die Lambda-Funktion wird täglich automatisch ausgeführt und die Ergebnisse in der Datenbank gespeichert.

## Features
- Bitcoin Preis-Monitoring in Echtzeit
- Moving Average Crossover Strategie
- Interaktives Backtesting mit anpassbaren Parametern
- Performance-Metriken Visualisierung
- Trade-History Tracking
- PostgreSQL Datenbankintegration für Trade-Logging

## Benötigte Pakete
- streamlit: Web Anwendungs-Framework
- pandas: Datenmanipulation und -analyse
- numpy: Numerische Berechnungen
- plotly: Interaktive Visualisierungen
- python-dotenv: Umgebungsvariablen-Management
- boto3: AWS SDK für Python
- ccxt: Kryptowährungs-Exchange API
- sqlalchemy: Datenbank ORM
- psycopg2-binary: PostgreSQL Adapter

## Repository Synchronisation

Um Ihr lokales Repository mit den neuesten Änderungen zu synchronisieren:

```bash
python sync_repo.py
```

Optionen:
- `--repo`: Alternative Repository URL angeben
- `--branch`: Anderen Branch angeben (Standard: main)

Beispiel:
```bash
python sync_repo.py --branch development