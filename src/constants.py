import os
from dotenv import load_dotenv

# 1. Try to load .env (this will work locally, but fail silently in GitHub)
load_dotenv()

# 2. Fetch the variables
MONGO_URI = os.getenv("MONGO_URI")
AV_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
DB_NAME = "financial-ingestion"
COLLECTION_NAME = "price_history"

# 3. Only raise an error if BOTH .env and GitHub Secrets are missing
if not MONGO_URI:
    raise ValueError("CRITICAL: MONGO_URI not found in environment or .env file!")

# Ingestion Settings
DEFAULT_INTERVAL = "1m"
DEFAULT_PERIOD = "1d"
MIN_PRICE_THRESHOLD = 0.0001
"""
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
"""