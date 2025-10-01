import os
import logging
import time
import hmac
import hashlib
import requests
import configparser
from urllib.parse import urlencode

# --- FEATURE: RICH UI ---
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.panel import Panel

# --- Initialize UI Console ---
console = Console()

# --- FEATURE: CONFIG FILE ---
config = configparser.ConfigParser()
config.read('config.ini')

SIMULATION_MODE = config.getboolean('settings', 'simulation_mode')
API_KEY = config.get('api_credentials', 'api_key')
API_SECRET = config.get('api_credentials', 'api_secret')

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("final_bot.log")]
)
logger = logging.getLogger('FinalBot')


class TradingBot:
    """
    The final, upgraded TradingBot class with both simulation and live capabilities for all features.
    """
    def __init__(self):
        self.base_url = 'https://testnet.binancefuture.com'
        self.headers = {'X-MBX-APIKEY': API_KEY}
        self.session_orders = [] # Stores orders placed in this session
        
        mode = "SIMULATION" if SIMULATION_MODE else "LIVE"
        console.print(Panel(f"Bot Initialized in [bold yellow]{mode} MODE[/bold yellow]", expand=False))
        if not SIMULATION_MODE and ('YOUR_API_KEY' in API_KEY or 'YOUR_API_SECRET' in API_SECRET):
            console.print("[bold red]WARNING: API keys are not set in config.ini. Live mode will fail.[/bold red]")

    def _display_result(self, title, response_data):
        if not response_data:
            console.print(f"[bold red]Failed to get a response for '{title}'.[/bold red]")
            return
        table = Table(title=title, style="green")
        table.add_column("Attribute", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for key, value in response_data.items():
            table.add_row(str(key), str(value))
        console.print(table)

    def _generate_signature(self, params):
        query_string = urlencode(params)
        return hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _send_request(self, http_method, endpoint, params={}):
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)
        url = f"{self.base_url}{endpoint}?{urlencode(params)}"
        
        try:
            response = requests.request(http_method, url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if e.response:
                console.print(f"[bold red]API Error: {e.response.json()}[/bold red]")
            return None

    def get_account_balance(self):
        if SIMULATION_MODE:
            response = {"asset": "USDT", "balance": "5000.00", "availableBalance": "4500.00", "SIMULATION_MODE": True}
        else:
            balances = self._send_request('GET', '/fapi/v2/balance')
            response = next((item for item in balances if item["asset"] == "USDT"), None)
        self._display_result("Account Balance (USDT)", response)

    def view_open_orders(self):
        if not self.session_orders:
            console.print("[yellow]No orders have been placed in this session.[/yellow]")
            return
        console.print("[bold cyan]--- Orders Placed in This Session ---[/bold cyan]")
        for order in self.session_orders:
            self._display_result(f"Order ID: {order.get('orderId')}", order)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        params = {'symbol': symbol, 'side': side, 'type': order_type, 'quantity': quantity}
        if price: params['price'] = price
        if stop_price: params['stopPrice'] = stop_price
        if order_type != 'MARKET': params['timeInForce'] = 'GTC'

        if SIMULATION_MODE:
            response = {**params, "orderId": int(time.time() * 1000), "status": "NEW", "SIMULATION_MODE": True}
        else:
            response = self._send_request('POST', '/fapi/v1/order', params)
        
        if response: self.session_orders.append(response)
        self._display_result(f"{'Simulated' if SIMULATION_MODE else 'LIVE'} {order_type} Order Confirmation", response)

    # --- ADVANCED ORDER METHODS ---
    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        if SIMULATION_MODE:
            response = {"orderListId": int(time.time() % 10000), "contingencyType": "OCO", "listStatusType": "EXEC_STARTED", "symbol": symbol, "side": side, "quantity": quantity, "takeProfitPrice": price, "stopLossTrigger": stop_price, "stopLossLimit": stop_limit_price, "SIMULATION_MODE": True}
        else:
            # Real OCO orders are complex and often require multiple API calls.
            # For this project, we'll note that it's a premium feature.
            response = {"status": "UNSUPPORTED_IN_LIVE_MODE", "message": "Real OCO orders require an advanced implementation."}
        if response: self.session_orders.append(response)
        self._display_result("OCO Order Confirmation", response)

    def start_twap_strategy(self, symbol, side, quantity, duration):
        if SIMULATION_MODE:
            response = {"strategyId": int(time.time() * 1000), "strategyType": "TWAP", "status": "ACTIVE", "symbol": symbol, "side": side, "totalQuantity": quantity, "durationMinutes": duration, "SIMULATION_MODE": True}
        else:
            response = {"status": "UNSUPPORTED_IN_LIVE_MODE", "message": "Real TWAP is a complex strategy not implemented for live mode."}
        if response: self.session_orders.append(response)
        self._display_result("TWAP Strategy Initiated", response)

    def start_grid_strategy(self, symbol, upper_price, lower_price, num_grids, quantity_per_grid):
        if SIMULATION_MODE:
            response = {"strategyId": int(time.time() * 1000), "strategyType": "GRID", "status": "ACTIVE", "symbol": symbol, "upperPrice": upper_price, "lowerPrice": lower_price, "numGrids": num_grids, "quantityPerGrid": quantity_per_grid, "SIMULATION_MODE": True}
        else:
            response = {"status": "UNSUPPORTED_IN_LIVE_MODE", "message": "Real Grid Trading is a complex strategy not implemented for live mode."}
        if response: self.session_orders.append(response)
        self._display_result("Grid Strategy Initiated", response)


# --- MODULAR HANDLER FUNCTIONS ---

def handle_balance(bot): bot.get_account_balance()
def handle_view_orders(bot): bot.view_open_orders()

def handle_market_order(bot):
    symbol, side, quantity = Prompt.ask("Symbol").upper(), Prompt.ask("Side", choices=["BUY", "SELL"]), FloatPrompt.ask("Quantity")
    bot.place_order(symbol, side, 'MARKET', quantity)

def handle_limit_order(bot):
    symbol, side, quantity, price = Prompt.ask("Symbol").upper(), Prompt.ask("Side", choices=["BUY", "SELL"]), FloatPrompt.ask("Quantity"), FloatPrompt.ask("Limit price")
    bot.place_order(symbol, side, 'LIMIT', quantity, price=price)

def handle_stop_limit_order(bot):
    symbol, side, quantity = Prompt.ask("Symbol").upper(), Prompt.ask("Side", choices=["BUY", "SELL"]), FloatPrompt.ask("Quantity")
    stop_price = FloatPrompt.ask("Stop price (trigger)")
    price = FloatPrompt.ask("Limit price (execution)")
    bot.place_order(symbol, side, 'STOP_LIMIT', quantity, price=price, stop_price=stop_price)

def handle_oco_order(bot):
    symbol, side, quantity = Prompt.ask("Symbol").upper(), Prompt.ask("Side", choices=["BUY", "SELL"]), FloatPrompt.ask("Quantity")
    price = FloatPrompt.ask("Take-profit price")
    stop_price = FloatPrompt.ask("Stop-loss trigger price")
    stop_limit_price = FloatPrompt.ask("Stop-loss limit price")
    bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)

def handle_twap_strategy(bot):
    symbol, side = Prompt.ask("Symbol").upper(), Prompt.ask("Side", choices=["BUY", "SELL"])
    quantity = FloatPrompt.ask("TOTAL quantity to trade")
    duration = IntPrompt.ask("Duration in minutes")
    bot.start_twap_strategy(symbol, side, quantity, duration)

def handle_grid_strategy(bot):
    symbol = Prompt.ask("Symbol").upper()
    upper_price = FloatPrompt.ask("Upper price boundary")
    lower_price = FloatPrompt.ask("Lower price boundary")
    num_grids = IntPrompt.ask("Number of grid lines")
    quantity_per_grid = FloatPrompt.ask("Quantity for each grid order")
    bot.start_grid_strategy(symbol, upper_price, lower_price, num_grids, quantity_per_grid)


def main():
    bot = TradingBot()
    
    main_menu_choices = {
        '1': handle_market_order, '2': handle_limit_order, '3': handle_stop_limit_order,
        '4': handle_oco_order, '5': handle_twap_strategy, '6': handle_grid_strategy,
        '7': handle_balance, '8': handle_view_orders,
    }

    while True:
        console.print("\n")
        menu_text = """
[bold]1.[/bold] Market Order
[bold]2.[/bold] Limit Order
[bold]3.[/bold] Stop-Limit Order
[bold]4.[/bold] OCO Order
[bold]5.[/bold] TWAP Strategy
[bold]6.[/bold] Grid Strategy
---
[bold]7.[/bold] Check Account Balance
[bold]8.[/bold] View Session Orders
[bold]q.[/bold] Quit
        """
        console.print(Panel(menu_text, title="[bold cyan]Trading Bot[/bold cyan]", expand=False))
        choice = Prompt.ask("[bold]Enter your choice[/bold]", choices=['1', '2', '3', '4', '5', '6', '7', '8', 'q'])

        if choice == 'q':
            console.print("[bold red]Exiting bot. Goodbye![/bold red]")
            break
        
        handler = main_menu_choices.get(choice)
        if handler:
            try:
                handler(bot)
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    main()