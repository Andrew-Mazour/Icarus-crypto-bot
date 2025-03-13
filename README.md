## 🚀 Crypto Trading Bot

This is an automated cryptocurrency trading bot that interacts with the Pump.fun API to buy and sell cryptocurrencies based on predefined trading strategies. The bot continuously monitors market trends and executes trades to maximize profitability.

## 🔥 Features

- **Automated Trading**: Executes buy and sell orders based on market conditions.

- **Pump.fun API Integration**: Interacts with the Pump.fun API for real-time trading.

- **Customizable Strategies**: Supports different trading strategies such as scalping, trend following, and arbitrage.

- **Risk Management**: Includes stop-loss and take-profit mechanisms.

-**Logging and Monitoring**: Keeps track of executed trades and market conditions.

## 📥 Installation

**Clone the repository**:

- git clone https://github.com/yourusername/Icarus-crypto-bot.git
- cd Icarus-trading-bot

**Create a virtual environment (optional but recommended)**:

- python -m venv venv
- source venv/bin/activate  # On Windows use: venv\Scripts\activate

**Install dependencies**:

- pip install -r requirements.txt

**Set up your API keys**:

- Obtain an API key from Pump.fun

**Create a .env file and add your credentials**:

- PUMP_FUN_API_KEY=your_api_key_here

## ⚙️ Configuration

Modify config.py to customize:

- Trading pairs

- Strategy parameters (e.g., buy/sell thresholds, stop-loss percentage)

- Logging settings

## 📈 Example Strategy

A simple strategy that buys when the price drops by 5% and sells when it increases by 10%:

BUY_THRESHOLD = -5  # Buy when price drops 5%  
SELL_THRESHOLD = 10  # Sell when price rises 10%  
STOP_LOSS = -8       # Stop-loss at 8%

## 📊 Logging and Monitoring

All trades and logs are stored in logs/trading.log. You can view live trades in the console output.

## ⚠️ Disclaimer

This bot is for educational purposes only. Trading cryptocurrencies carries risk, and you should use this bot at your own discretion. Always trade responsibly.

## 🤝 Contributions

Feel free to submit issues and pull requests to improve this project.
