from datetime import datetime
from schema.agentSchema import StockPriceInputSchema, StockPriceOutputSchema
from service.priceService import fetchLivePrice, fetchHistoricalPrices

# LangChain/Groq tool definition — used in plannerNode for LLM tool calling
STOCK_PRICE_TOOL_DEFINITION = {
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Fetch current or historical stock price data for NVDA or TSLA. Use when the question involves prices, returns, or price movements.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "enum": ["NVDA", "TSLA"],
                    "description": "The stock ticker symbol"
                },
                "startDate": {
                    "type": "string",
                    "description": "Start date for historical data in YYYY-MM-DD format. Omit for current price only."
                },
                "endDate": {
                    "type": "string",
                    "description": "End date for historical data in YYYY-MM-DD format. Defaults to today."
                }
            },
            "required": ["ticker"]
        }
    }
}

async def runStockPriceTool(inputData: StockPriceInputSchema) -> StockPriceOutputSchema:
    """
    Run the stock price tool.
    If startDate is provided → fetch historical data.
    Otherwise → fetch current live price only.
    """
    try:
        if inputData.startDate:
            endDate = inputData.endDate or datetime.utcnow().strftime("%Y-%m-%d")
            return await fetchHistoricalPrices(
                ticker=inputData.ticker.value,
                startDate=inputData.startDate,
                endDate=endDate
            )
        else:
            return await fetchLivePrice(ticker=inputData.ticker.value)

    except Exception as e:
        return StockPriceOutputSchema(
            ticker=inputData.ticker.value,
            currentPrice=0.0,
            change=0.0,
            changePercent=0.0,
            error=f"Price fetch failed: {str(e)}"
        )
