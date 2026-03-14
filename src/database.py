import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from src.constants import MONGO_URI, DB_NAME, COLLECTION_NAME

logger = logging.getLogger(__name__)

def get_database():
    """
    Establish a connection to MongoDB Atlas and return the database object.
    """
    try:
        # Connect to Atlas with a 5-second timeout
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Verify connection by 'pinging' the server
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB Atlas!")
        
        return client[DB_NAME]
    except ConnectionFailure:
        logger.error("Could not connect to Atlas. Check your Network Access/IP Whitelist.")
        raise
    except OperationFailure as e:
        logger.error(f"Authentication failed. Check your username/password in .env: {e}")
        raise

def setup_timeseries(db):
    """
    Converts a standard collection into an optimized Time-Series collection.
    """
    try:
        if COLLECTION_NAME not in db.list_collection_names():
            db.create_collection(
                COLLECTION_NAME,
                timeseries={
                    "timeField": "timestamp",
                    "metaField": "symbol",
                    "granularity": "minutes"
                }
            )
            logger.info(f"Created Time-Series collection: {COLLECTION_NAME}")
    except Exception as e:
        logger.warning(f"ℹCollection setup note: {e}")