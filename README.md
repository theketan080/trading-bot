<!-- Binance Futures CLI Bot
A command-line trading bot for the Binance USDT-M Futures market, built as a solution for a development task. This project features a modular architecture and offers two modes of operation: a user-friendly interactive menu and direct command-line execution for automation.

 Key Features
Dual Execution Modes: Run the bot via a rich, user-friendly interactive menu or through direct command-line arguments for scripting and automation.

Rich CLI Interface: The interactive mode uses the rich library for a modern experience with styled menus, color-coded prompts, and neatly formatted tables.

Bonus Feature Integration: Includes a "Fear & Greed Index" reader to provide market sentiment data directly in the interface.

Modular Architecture: Source code is professionally organized into core services (client, config, logger), utilities (validation), and individual scripts for each function.

External Configuration: All settings, including the operating mode and API credentials, are managed through a simple config.ini file.

Comprehensive Order Support: Implements mandatory orders (Market, Limit), bonus advanced orders (Stop-Limit), and simulated advanced strategies (OCO, TWAP, Grid).

Structured Logging: All actions, API calls, and errors are logged with timestamps to a bot.log file for easy debugging.

 Project Structure
/
├── src/
│   ├── core/
│   ├── utils/
│   └── advanced/
│
├── interactive_bot.py
├── config.ini
├── requirements.txt
├── Fear_and_Greed_Index.csv
└── README.md

 Installation and Setup
 Prerequisites
Python 3.9 or higher

Git

 Steps
Clone the repository:

git clone [your-repository-url]

Navigate to the project directory:

cd [your-repository-name]

Install dependencies:
The required libraries (requests, rich, pandas) are listed in requirements.txt.

pip install -r requirements.txt

Download External Data:

Download the Fear_and_Greed_Index.csv file from the link provided in the assignment.

Place this file in the root directory of the project.

Configure the bot:
Create a config.ini file in the root directory by copying the example below.

[settings]
# Set to true for simulation, false for live testnet trading.
simulation_mode = True

[api_credentials]
# IMPORTANT: Only needed when simulation_mode is false.
api_key = YOUR_API_KEY_HERE
api_secret = YOUR_API_SECRET_HERE

Set simulation_mode to true for testing or false for live trading.

If live, add your Binance Testnet API key and secret.

 Usage
This bot can be operated in two distinct ways:

1. Interactive Mode (Recommended)
For a user-friendly menu with all features, run the main interactive script.

py interactive_bot.py

2. Direct Command Mode
To execute a specific order type directly for automation or scripting, you can run the individual scripts from the root project folder.

Market Order

python src/market_order.py BTCUSDT BUY 0.001

Limit Order

python src/limit_order.py ETHUSDT SELL 0.01 3000

 License
This project is licensed under the MIT License. -->