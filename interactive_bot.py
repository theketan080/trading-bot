import sys
import os
import traceback

# This line adds your 'src' folder to Python's path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# --- RICH UI IMPORTS ---
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, FloatPrompt, IntPrompt
from rich.panel import Panel

# --- CORE BOT IMPORTS ---
from core.client import TradingBot
from core.logger import setup_logger
from core.config import SIMULATION_MODE

# --- SETUP ---
console = Console()
logger = setup_logger()


# --- HANDLER FUNCTIONS (UI Logic) ---
def handle_market_order(bot: TradingBot):
    symbol = Prompt.ask("Enter symbol").upper()
    side = Prompt.ask("Enter side", choices=["BUY", "SELL"])
    quantity = FloatPrompt.ask("Enter quantity")
    params = {'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': quantity}
    bot.place_order(params)

def handle_limit_order(bot: TradingBot):
    symbol = Prompt.ask("Symbol").upper()
    side = Prompt.ask("Side", choices=["BUY", "SELL"])
    quantity = FloatPrompt.ask("Quantity")
    price = FloatPrompt.ask("Limit price")
    params = {'symbol': symbol, 'side': side, 'type': 'LIMIT', 'quantity': quantity, 'price': price, 'timeInForce': 'GTC'}
    bot.place_order(params)

def handle_stop_limit_order(bot: TradingBot):
    symbol = Prompt.ask("Symbol").upper()
    side = Prompt.ask("Side", choices=["BUY", "SELL"])
    quantity = FloatPrompt.ask("Quantity")
    stop_price = FloatPrompt.ask("Stop price (trigger)")
    price = FloatPrompt.ask("Limit price (execution)")
    params = {'symbol': symbol, 'side': side, 'type': 'STOP_LIMIT', 'quantity': quantity, 'price': price, 'stopPrice': stop_price, 'timeInForce': 'GTC'}
    bot.place_order(params)

def handle_oco_order(bot: TradingBot):
    symbol = Prompt.ask("Symbol").upper()
    side = Prompt.ask("Side", choices=["BUY", "SELL"])
    quantity = FloatPrompt.ask("Quantity")
    price = FloatPrompt.ask("Take-profit price")
    stop_price = FloatPrompt.ask("Stop-loss trigger price")
    stop_limit_price = FloatPrompt.ask("Stop-loss limit price")
    params = {'symbol': symbol, 'side': side, 'quantity': quantity, 'price': price, 'stopPrice': stop_price, 'stopLimitPrice': stop_limit_price}
    bot.place_oco_order(params)

def handle_twap_strategy(bot: TradingBot):
    symbol = Prompt.ask("Symbol").upper()
    side = Prompt.ask("Side", choices=["BUY", "SELL"])
    quantity = FloatPrompt.ask("TOTAL quantity")
    duration = IntPrompt.ask("Duration in minutes")
    params = {'symbol': symbol, 'side': side, 'quantity': quantity, 'durationMinutes': duration}
    bot.start_twap_strategy(params)

def handle_grid_strategy(bot: TradingBot):
    symbol = Prompt.ask("Symbol").upper()
    upper = FloatPrompt.ask("Upper price boundary")
    lower = FloatPrompt.ask("Lower price boundary")
    grids = IntPrompt.ask("Number of grid lines")
    quantity = FloatPrompt.ask("Quantity for each grid order")
    params = {'symbol': symbol, 'upperPrice': upper, 'lowerPrice': lower, 'numGrids': grids, 'quantityPerGrid': quantity}
    bot.start_grid_strategy(params)

def handle_fear_and_greed(bot: TradingBot):
    bot.get_fear_and_greed()

# --- MAIN APPLICATION LOOP ---
def main():
    bot = TradingBot()
    
    menu_choices = {
        '1': handle_market_order, '2': handle_limit_order, '3': handle_stop_limit_order,
        '4': handle_oco_order, '5': handle_twap_strategy, '6': handle_grid_strategy,
        'fg': handle_fear_and_greed,
    }

    while True:
        console.print("\n")
        mode_text = "[bold yellow]SIMULATION MODE[/bold yellow]" if SIMULATION_MODE else "[bold green]LIVE MODE[/bold green]"
        
        menu_text = """
[bold]1.[/bold] Market Order  [bold]2.[/bold] Limit Order   [bold]3.[/bold] Stop-Limit
[bold]4.[/bold] OCO Order     [bold]5.[/bold] TWAP Strategy [bold]6.[/bold] Grid Strategy
---
[bold]fg.[/bold] Check Fear & Greed Index
[bold]q.[/bold] Quit
        """
        console.print(Panel(menu_text, title=f"[bold cyan]Interactive Trading Bot[/bold cyan]", subtitle=mode_text, expand=False))
        
        choice = Prompt.ask("[bold]Enter your choice[/bold]", choices=['1', '2', '3', '4', '5', '6', 'fg', 'q'])
        
        if choice == 'q':
            console.print("[bold red]Goodbye![/bold red]")
            break
        
        handler = menu_choices.get(choice)
        if handler:
            handler(bot)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"A critical error occurred: {traceback.format_exc()}")
        console.print(f"[bold red]A critical error occurred. Check bot.log for details: {e}[/bold red]")
