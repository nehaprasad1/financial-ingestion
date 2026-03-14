import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Database Configurations
MONGO_URI = os.getenv("MONGO_URI")
AV_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
# Fallback check (Professional touch)
DB_NAME = "financial-ingestion"
COLLECTION_NAME = "price_history"
if not MONGO_URI:
    raise ValueError(" MONGO_URI not found! Make sure your .env file is in the root folder.")
# Ingestion Settings
DEFAULT_INTERVAL = "1m"
DEFAULT_PERIOD = "1d"

# Logic Constraints
MIN_PRICE_THRESHOLD = 0.0001