import httpx
from schema.agentSchema import StockPriceOutputSchema, PricePointSchema
from constant.appConstants import ALPHA_VANTAGE_BASE_URL, ALPHA_VANTAGE_KEY

async def fetchLivePrice(ticker: str) -> StockPriceOutputSchema:
    """
    Fetch the current stock price for a ticker from Alpha Vantage.
    Uses GLOBAL_QUOTE function — single API call, minimal quota usage.
    Free tier: 25 requests/day — sufficient for NVDA + TSLA with caching.
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(ALPHA_VANTAGE_BASE_URL, params={
            "function":   "GLOBAL_QUOTE",
            "symbol":     ticker,
            "apikey":     ALPHA_VANTAGE_KEY
        })
        response.raise_for_status()
        data = response.json()

    quoteData = data.get("Global Quote", {})

    if not quoteData:
        return StockPriceOutputSchema(
            ticker=ticker,
            currentPrice=0.0,
            change=0.0,
            changePercent=0.0,
            error="No price data returned from Alpha Vantage"
        )

    rawPrice         = quoteData.get("05. price", "0")
    rawChange        = quoteData.get("09. change", "0")
    rawChangePercent = quoteData.get("10. change percent", "0%").replace("%", "")

    return StockPriceOutputSchema(
        ticker=ticker,
        currentPrice=float(rawPrice),
        change=float(rawChange),
        changePercent=float(rawChangePercent)
    )

async def fetchHistoricalPrices(
    ticker:    str,
    startDate: str | None = None,
    endDate:   str | None = None
) -> StockPriceOutputSchema:
    """
    Fetch daily historical OHLCV data from Alpha Vantage.
    Uses TIME_SERIES_DAILY_ADJUSTED function.
    Filters by startDate/endDate if provided.
    """
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(ALPHA_VANTAGE_BASE_URL, params={
            "function":   "TIME_SERIES_DAILY_ADJUSTED",
            "symbol":     ticker,
            "outputsize": "compact",    # last 100 trading days
            "apikey":     ALPHA_VANTAGE_KEY
        })
        response.raise_for_status()
        data = response.json()

    timeSeriesRaw = data.get("Time Series (Daily)", {})

    pricePoints = []
    for dateStr, ohlcv in timeSeriesRaw.items():
        if startDate and dateStr < startDate:
            continue
        if endDate and dateStr > endDate:
            continue
        pricePoints.append(PricePointSchema(
            date=dateStr,
            open=float(ohlcv.get("1. open", 0)),
            high=float(ohlcv.get("2. high", 0)),
            low=float(ohlcv.get("3. low", 0)),
            close=float(ohlcv.get("4. close", 0)),
            volume=int(ohlcv.get("6. volume", 0))
        ))

    # Sort ascending by date
    pricePoints.sort(key=lambda x: x.date)

    # Get current price from first entry in live API response
    latestEntry  = next(iter(timeSeriesRaw.values()), {})
    currentPrice = float(latestEntry.get("4. close", 0))

    return StockPriceOutputSchema(
        ticker=ticker,
        currentPrice=currentPrice,
        change=0.0,
        changePercent=0.0,
        historicalData=pricePoints
    )
