import time
import hmac
import hashlib
import requests
import pandas as pd
import os
from urllib.parse import urlencode
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .config import SIMULATION_MODE, API_KEY, API_SECRET
from .logger import setup_logger

logger = setup_logger()
console = Console()

class TradingBot:
    def __init__(self):
        self.base_url = 'https://testnet.binancefuture.com'
        self.headers = {'X-MBX-APIKEY': API_KEY}
        logger.info(f"Client initialized in {'SIMULATION' if SIMULATION_MODE else 'LIVE'} mode.")

    def _display_result(self, title, response_data):
        """Helper function to display results in a rich table."""
        if not response_data:
            console.print(f"[bold red]Failed to get a response for '{title}'.[/bold red]")
            return
        table = Table(title=title, style="green")
        table.add_column("Attribute", style="cyan")
        table.add_column("Value", style="magenta")
        for key, value in response_data.items():
            table.add_row(str(key), str(value))
        console.print(table)

    def _send_request(self, http_method, endpoint, params={}):
        # Placeholder for live trading logic
        console.print("[yellow]Live mode not fully implemented in this example.[/yellow]")
        return {"status": "LIVE_MODE_TODO", **params}

    def place_order(self, params):
        """Places simple orders (Market, Limit, Stop-Limit)."""
        logger.info(f"Placing order with params: {params}")
        if SIMULATION_MODE:
            response = {**params, "orderId": int(time.time() * 1000), "status": "SIMULATED_NEW"}
            self._display_result(f"Simulated {params.get('type')} Order", response)
        else:
            response = self._send_request('POST', '/fapi/v1/order', params)
            self._display_result(f"Live {params.get('type')} Order Response", response)
        return response

    def place_oco_order(self, params):
        """Simulates placing an OCO order."""
        logger.info(f"Simulating OCO order with params: {params}")
        if SIMULATION_MODE:
            response = {"orderListId": int(time.time() % 10000), "contingencyType": "OCO", "status": "SIMULATED_NEW", **params}
            self._display_result("Simulated OCO Order", response)
        else:
            response = {"status": "LIVE_MODE_TODO", "message": "Real OCO orders are complex."}
        return response

    def start_twap_strategy(self, params):
        """Simulates starting a TWAP strategy."""
        logger.info(f"Simulating TWAP strategy with params: {params}")
        if SIMULATION_MODE:
            response = {"strategyId": int(time.time() * 1000), "strategyType": "TWAP", "status": "SIMULATED_ACTIVE", **params}
            self._display_result("Simulated TWAP Strategy", response)
        else:
            response = {"status": "LIVE_MODE_TODO", "message": "Real TWAP is a complex strategy."}
        return response
    
    def start_grid_strategy(self, params):
        """Simulates starting a Grid strategy."""
        logger.info(f"Simulating Grid strategy with params: {params}")
        if SIMULATION_MODE:
            response = {"strategyId": int(time.time() * 1000), "strategyType": "GRID", "status": "SIMULATED_ACTIVE", **params}
            self._display_result("Simulated Grid Strategy", response)
        else:
            response = {"status": "LIVE_MODE_TODO", "message": "Real Grid Trading is a complex strategy."}
        return response

    def get_fear_and_greed(self):
        """Reads and displays the Fear & Greed Index from the local CSV file."""
        logger.info("Fetching Fear & Greed Index.")
        
        # Build the path to the CSV file in the project's root
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Fear_and_Greed_Index.csv')
        
        try:
            df = pd.read_csv(csv_path)
            # Get the most recent entry (last row)
            latest_entry = df.iloc[-1]
            
            value = latest_entry['value']
            classification = latest_entry['classification']
            
            # Use rich to display it with color coding
            color = "red" if value <= 25 else "green" if value >= 75 else "yellow"
            
            console.print("\n")
            console.print(Panel(f"Latest Value: [bold {color}]{value}[/bold {color}]\nClassification: [bold {color}]{classification}[/bold {color}]", title="[bold cyan]😨 Fear & Greed Index 🤑[/bold cyan]", expand=False))
            
        except FileNotFoundError:
            logger.error("Fear_and_Greed_Index.csv not found in the root directory.")
            console.print("[bold red]Error: Fear_and_Greed_Index.csv not found. Please download it and place it in the main project folder.[/bold red]")
        except Exception as e:
            logger.error(f"Failed to read or parse Fear & Greed Index file: {e}")
            console.print(f"[bold red]An error occurred while reading the index file: {e}[/bold red]")
