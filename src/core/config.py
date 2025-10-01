import configparser
import os

# Build the path to the config file in the project's root directory
# This clever pathing allows scripts inside /src to find the config.ini file at the top level
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)

# Make settings available for import by other modules
SIMULATION_MODE = config.getboolean('settings', 'simulation_mode')
API_KEY = config.get('api_credentials', 'api_key')
API_SECRET = config.get('api_credentials', 'api_secret')