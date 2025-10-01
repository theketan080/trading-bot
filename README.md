<!--  # Final Trading Bot

This project is a sophisticated command-line trading bot designed for the Binance Futures Testnet. It was developed as a comprehensive solution to an application task, featuring a rich user interface, dual-mode operation (live and simulation), and support for various order types and strategies.

## ✨ Key Features

  - **Dual Mode Operation:** Seamlessly switch between a safe **Simulation Mode** (no API keys needed) and a **Live Mode** that connects directly to the Binance Testnet.
  - **Rich CLI Interface:** Built with the `rich` library for a modern, user-friendly experience with styled menus, color-coded prompts, and neatly formatted tables for output.
  - **External Configuration:** All settings, including the operating mode and API credentials, are managed through a simple `config.ini` file, so no code changes are needed to go live.
  - **Comprehensive Order Support:** Implements standard orders (Market, Limit, Stop-Limit) and provides a simulated framework for advanced strategies like OCO, TWAP, and Grid Trading.
  - **Account Management:** Includes essential functions to check your Testnet account balance and view a history of orders placed during the current session.
  - **Robust Logging:** Automatically logs all major actions, API calls, and errors to a `final_bot.log` file for easy debugging and tracking.

## 📸 Demo

The bot features a clean, interactive panel for navigation and presents all data in organized tables.

```
┌───────────────────────────────────┐
│     Final Trading Bot             │
└───────────────────────────────────┘
┌─────────────────────────────────────────────────┐
│ ╭─ Binance Trading Bot Menu ──────────────────╮ │
│ │                                             │ │
│ │ 1. Market Order                             │ │
│ │ 2. Limit Order                              │ │
│ │ 3. Stop-Limit Order                         │ │
│ │ 4. OCO Order                                │ │
│ │ 5. TWAP Strategy                            │ │
│ │ 6. Grid Strategy                            │ │
│ │ ---                                         │ │
│ │ 7. Check Account Balance                    │ │
│ │ 8. View Session Orders                      │ │
│ │ q. Quit                                     │ │
│ │                                             │ │
│ ╰─────────────────────────────────────────────╯ │
└─────────────────────────────────────────────────┘
> Enter your choice: 2
> Enter symbol: BTCUSDT
> Enter side: BUY
> Enter quantity: 0.01
> Enter limit price: 55000

┌─── Simulated LIMIT Order Confirmation ───┐
│     Attribute │ Value                  │
├───────────────┼────────────────────────┤
│        symbol │ BTCUSDT                │
│          side │ BUY                    │
│          type │ LIMIT                  │
│      quantity │ 0.01                   │
│         price │ 55000.0                │
│   timeInForce │ GTC                    │
│       orderId │ 1727802675000          │
│        status │ NEW                    │
│ SIMULATION... │ True                   │
└───────────────┴────────────────────────┘
```

##  Installation and Setup

Follow these steps to get the bot running on your local machine.

###  Prerequisites

  * Python 3.9 or higher

###  Steps

1.  **Clone the repository (or download the files):**

    ```bash
    git clone [your-repository-url]
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd TradingBor
    ```

3.  **Install dependencies:**
    The project requires `requests` and `rich`. Install them using the `requirements.txt` file.

    ```bash
    py -m pip install -r requirements.txt
    ```

4.  **Configure the bot:**
    Create a file named `config.ini` and paste the following content. Edit the values as needed.

    ```ini
    [settings]
    # Set to true to run in simulation mode without real orders.
    # Set to false to run in live mode with your testnet account.
    simulation_mode = True

    [api_credentials]
    # IMPORTANT: Only needed when simulation_mode is false.
    # Get these from your Binance Testnet account.
    api_key = YOUR_API_KEY_HERE
    api_secret = YOUR_API_SECRET_HERE
    ```

##  How to Run

Once the setup and configuration are complete, run the bot from your terminal with the following command:

```bash
py final_bot.py
```

##  Project Structure

The project directory contains the following key files:

```
/
├── final_bot.py        # The main application script
├── config.ini          # Configuration file for settings and API keys
├── requirements.txt    # List of Python dependencies
└── README.md           # This file
```

##  License

This project is licensed under the MIT License.  -->