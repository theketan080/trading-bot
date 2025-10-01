import argparse
import sys
# This adjusts the path to allow imports from the parent directory (src)
sys.path.append(sys.path[0] + '/..')
from core.client import TradingBot
from core.logger import setup_logger
# --- FIX IS HERE ---
from utils.validation import validate_order_inputs

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="Place a Market Order on Binance Futures.")
    parser.add_argument("symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("side", type=str, choices=['BUY', 'SELL'], help="Order side: BUY or SELL")
    parser.add_argument("quantity", type=float, help="Order quantity")
    args = parser.parse_args()

    try:
        # --- AND FIX IS HERE ---
        validate_order_inputs(args.symbol, args.side, args.quantity)
        
        bot = TradingBot()
        params = {
            'symbol': args.symbol.upper(),
            'side': args.side.upper(),
            'type': 'MARKET',
            'quantity': args.quantity,
        }
        bot.place_order(params)
        
    except ValueError as e:
        logger.error(f"Input validation failed: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred. See bot.log for details.")

if __name__ == "__main__":
    main()