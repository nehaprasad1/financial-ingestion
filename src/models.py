from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class FinancialRecord(BaseModel):
    """
    Schema for a single financial data point.
    Pydantic ensures data types are correct before they reach MongoDB.
    """
    symbol: str = Field(..., description="The ticker symbol (e.g., NVDA, BTC-USD)")
    timestamp: datetime = Field(..., description="The time the price was recorded")
    price: float = Field(..., gt=0, description="The closing price, must be greater than 0")
    volume: int = Field(..., ge=0, description="The trading volume")
    high: Optional[float] = None
    low: Optional[float] = None

    @field_validator('symbol')
    @classmethod
    def convert_uppercase(cls, v: str) -> str:
        """Automatically converts ticker symbols to uppercase."""
        return v.upper()

    class Config:
        # This helps Pydantic work smoothly with various data sources
        populate_by_name = True