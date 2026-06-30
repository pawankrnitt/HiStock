from enum import Enum

class ToolNameEnum(str, Enum):
    STOCK_PRICE        = "get_stock_price"
    SEARCH_DOCUMENTS   = "search_documents"
    SEARCH_NEWS        = "search_news"
    CALCULATE_RATIO    = "calculate_ratio"
