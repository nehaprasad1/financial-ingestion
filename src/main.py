import time
import yaml
import logging
import os
from src.database import get_database, setup_timeseries
from src.ingestion import fetch_market_data
import sys
# Set up professional logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """
    Main orchestrator for the financial ingestion pipeline.
    Loads config, connects to Atlas, and handles the ingestion loop.
    """
    # 1. Load Configuration
    config_path = os.path.join("config", "config.yaml")
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        return

    # 2. Setup Database Connection
    try:
        db = get_database()
        setup_timeseries(db)
        # Collection name defined in src/constants.py
        from src.constants import COLLECTION_NAME
        collection = db[COLLECTION_NAME] 
    except Exception as e:
        logger.error(f"DB setup failed: {e}")
        return

    # 3. Execution Loop
    assets = config.get('assets', [])
    # Default to 3600s (1 hour) to stay within Alpha Vantage free tier limits
    interval = config.get('pipeline_settings', {}).get('update_interval_seconds', 3600)

    logger.info(f"Starting pipeline for {len(assets)} assets...")

    try:
        while True:
            for index, asset in enumerate(assets):
                symbol = asset['symbol']
                
                # Fetch and Validate data from Alpha Vantage
                record = fetch_market_data(symbol)
                
                if record:
                    # model_dump() converts our Pydantic object to a Dictionary for MongoDB
                    collection.insert_one(record.model_dump())
                    logger.info(f"Saved {symbol} to Atlas at ${record.price}")
                else:
                    logger.warning(f" Skipping {symbol} due to fetch error.")

                # RATE LIMIT PROTECTION:
                # Alpha Vantage Free Tier allows 5 requests per minute.
                # If we have more assets in the list, we wait 15 seconds between them.
                if index < len(assets) - 1:
                    logger.info("Waiting 15 sec...")
                    time.sleep(15)
            # --- CI/CD LOGIC ---
            if "--once" in sys.argv:
                logger.info("Single cycle mode active. Exiting successfully.")
                break
            logger.info(f"Cycle complete. Sleeping for {interval}s...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("Pipeline stopped by user.")
  
           
if __name__ == "__main__":
    run_pipeline()