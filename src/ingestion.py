import requests
import logging
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.constants import AV_API_KEY
from src.models import FinancialRecord

logger = logging.getLogger(__name__)

def get_session():
    """Creates a requests session with retry logic."""
    session = requests.Session()
    # Retry strategy: 3 retries, backoff factor helps wait between tries
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session

# Create a global session to reuse the connection
http_session = get_session()

def fetch_market_data(symbol):
    """Fetches the latest price from Alpha Vantage with retry logic."""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={AV_API_KEY}"
    
    try:
        response = http_session.get(url, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        data = response.json()
        
        quote = data.get("Global Quote", {})
        
        if not quote:
            # Check for API-specific error messages (like rate limit notes)
            if "Note" in data:
                logger.warning(f"Alpha Vantage API Note: {data['Note']}")
            return None

        return FinancialRecord(
            symbol=symbol,
            timestamp=datetime.now(),
            price=float(quote['05. price']),
            volume=int(quote['06. volume']),
            high=float(quote['03. high']),
            low=float(quote['04. low'])
        )
    except Exception as e:
        logger.error(f" Connection Error for {symbol}: {e}")
        return None