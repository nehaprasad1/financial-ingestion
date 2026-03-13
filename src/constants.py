import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Database Configurations
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "finance_db"
COLLECTION_NAME = "price_history"

# Ingestion Settings
DEFAULT_INTERVAL = "1m"
DEFAULT_PERIOD = "1d"

# Logic Constraints
MIN_PRICE_THRESHOLD = 0.0001