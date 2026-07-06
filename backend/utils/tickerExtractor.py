import re
from constant.appConstants import SUPPORTED_TICKERS

def extractTickersFromText(text: str) -> list[str]:
    """Find which supported tickers are mentioned in a block of text."""
    textUpper = text.upper()
    return [ticker for ticker in SUPPORTED_TICKERS if ticker in textUpper]
