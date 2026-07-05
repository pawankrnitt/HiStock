# worker/priceTickerWorker.py
# Responsibility: Background asyncio loop that pushes live price updates
# to all active session rooms every PRICE_POLL_INTERVAL_SECONDS.
# Only polls tickers that have been mentioned in each session's conversation.

import asyncio
from socketio_layer.socketServer import sio
from service.redisService import getActiveSessions, getCachedPrice, setCachedPrice
from service.priceService import fetchLivePrice
from schema.socketSchema import PriceUpdateEventSchema
from enums.socketEventEnum import SocketEventEnum
from constant.appConstants import PRICE_POLL_INTERVAL_SECONDS, SUPPORTED_TICKERS

async def startPriceTickerWorker():
    """
    Long-running background task — started on FastAPI startup, cancelled on shutdown.
    Every PRICE_POLL_INTERVAL_SECONDS seconds:
      1. Read active sessions from Redis
      2. Collect unique tickers mentioned across all sessions
      3. For each ticker: check Redis cache → fetch from Alpha Vantage if expired
      4. Emit price_update to each relevant session room
    """
    print("[worker] Price ticker worker started")

    while True:
        try:
            await asyncio.sleep(PRICE_POLL_INTERVAL_SECONDS)

            activeSessions = await getActiveSessions()
            if not activeSessions:
                continue

            # Collect all unique tickers across all active sessions
            allTickers = set()
            for session in activeSessions:
                mentionedTickers = session.get("mentionedTickers", [])
                if mentionedTickers:
                    allTickers.update(mentionedTickers)

            # If no tickers mentioned yet, push default supported tickers
            # so users see price movement even before asking a question
            if not allTickers:
                allTickers = set(SUPPORTED_TICKERS)

            # Fetch price for each unique ticker (with cache check)
            priceDataMap = {}
            for ticker in allTickers:
                try:
                    # Check Redis cache first
                    cached = await getCachedPrice(ticker)
                    if cached:
                        priceDataMap[ticker] = cached
                        continue

                    # Cache miss — fetch from Alpha Vantage
                    priceOutput = await fetchLivePrice(ticker)
                    if not priceOutput.error:
                        priceDict = {
                            "ticker":        priceOutput.ticker,
                            "price":         priceOutput.currentPrice,
                            "change":        priceOutput.change,
                            "changePercent": priceOutput.changePercent
                        }
                        await setCachedPrice(ticker, priceDict)
                        priceDataMap[ticker] = priceDict

                except Exception as e:
                    print(f"[worker] Error fetching price for {ticker}: {e}")

            # Emit price updates to each active session room
            for session in activeSessions:
                sessionId        = session["sessionId"]
                mentionedTickers = session.get("mentionedTickers", [])
                tickersToSend    = mentionedTickers if mentionedTickers else list(SUPPORTED_TICKERS)

                for ticker in tickersToSend:
                    priceData = priceDataMap.get(ticker)
                    if not priceData:
                        continue

                    payload = PriceUpdateEventSchema(
                        ticker=priceData["ticker"],
                        price=priceData["price"],
                        change=priceData["change"],
                        changePercent=priceData["changePercent"]
                    )
                    await sio.emit(
                        SocketEventEnum.PRICE_UPDATE,
                        payload.model_dump(),
                        room=sessionId
                    )

        except asyncio.CancelledError:
            print("[worker] Price ticker worker stopped")
            break
        except Exception as e:
            print(f"[worker] Price ticker error: {e}")
            # Don't crash the worker — log and continue next cycle
            await asyncio.sleep(PRICE_POLL_INTERVAL_SECONDS)
