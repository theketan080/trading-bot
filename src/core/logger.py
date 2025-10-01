import logging
import os

# Build the path to the log file in the project's root directory
log_path = os.path.join(os.path.dirname(__file__), '..', '..', 'bot.log')

def setup_logger():
    """Sets up a structured logger to output to the root bot.log file."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler() # Also print logs to the console
        ]
    )
    return logging.getLogger(__name__)