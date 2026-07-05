# service/redisService.py
# Responsibility: All Redis read/write operations for caching, active session
# tracking, and socket-to-user mapping. No Socket.io code here — pure data layer.
# All functions gracefully handle the case where Redis is not configured (returns
# safe defaults) — allows the app to run locally without Upstash for development.

import json
from db.redisClient import getRedisClient
from constant.appConstants import (
    REDIS_PRICE_TTL,
    REDIS_ACTIVE_SESSION_TTL,
    REDIS_SOCKET_MAP_TTL,
    REDIS_KEY_PRICE_CACHE,
    REDIS_KEY_ACTIVE_SESSIONS,
    REDIS_KEY_SOCKET_USER_MAP,
    REDIS_KEY_SESSION_TICKERS,
    RATE_LIMIT_KEY_PREFIX,
)

# ── Price cache ────────────────────────────────────────────────────────────────

async def getCachedPrice(ticker: str) -> dict | None:
    """Return cached price dict for a ticker, or None if not cached/expired."""
    client = await getRedisClient()
    if not client:
        return None
    cacheKey  = f"{REDIS_KEY_PRICE_CACHE}:{ticker}"
    cached    = await client.get(cacheKey)
    return json.loads(cached) if cached else None

async def setCachedPrice(ticker: str, priceData: dict, ttl: int = REDIS_PRICE_TTL) -> None:
    """Cache a price dict for `ttl` seconds — avoids hammering Alpha Vantage's rate limit."""
    client = await getRedisClient()
    if not client:
        return
    cacheKey = f"{REDIS_KEY_PRICE_CACHE}:{ticker}"
    await client.set(cacheKey, json.dumps(priceData), ex=ttl)

# ── Active session tracking (used by the price ticker worker) ──────────────────

async def addUserToActiveSession(sessionId: str, userId: str) -> None:
    """
    Add a session to the active sessions list (idempotent) so the price ticker
    worker knows to push updates to this room.
    """
    client = await getRedisClient()
    if not client:
        return
    activeSessions  = await getActiveSessions()

    existing = next((s for s in activeSessions if s["sessionId"] == sessionId), None)
    if existing:
        if userId not in existing["memberIds"]:
            existing["memberIds"].append(userId)
    else:
        activeSessions.append({
            "sessionId":        sessionId,
            "memberIds":        [userId],
            "mentionedTickers": []
        })

    await client.set(
        REDIS_KEY_ACTIVE_SESSIONS,
        json.dumps(activeSessions),
        ex=REDIS_ACTIVE_SESSION_TTL
    )

async def removeUserFromActiveSession(sessionId: str, userId: str) -> None:
    """Remove a user from a session's active member list. Drops the session entirely if empty."""
    client = await getRedisClient()
    if not client:
        return
    activeSessions  = await getActiveSessions()

    updatedSessions = []
    for session in activeSessions:
        if session["sessionId"] == sessionId:
            session["memberIds"] = [m for m in session["memberIds"] if m != userId]
            if session["memberIds"]:
                updatedSessions.append(session)
            # if empty, drop the session from active tracking
        else:
            updatedSessions.append(session)

    await client.set(
        REDIS_KEY_ACTIVE_SESSIONS,
        json.dumps(updatedSessions),
        ex=REDIS_ACTIVE_SESSION_TTL
    )

async def getActiveSessions() -> list[dict]:
    """Return the full list of currently active sessions (used by price ticker worker)."""
    client = await getRedisClient()
    if not client:
        return []
    raw    = await client.get(REDIS_KEY_ACTIVE_SESSIONS)
    return json.loads(raw) if raw else []

async def addTickersToSession(sessionId: str, tickers: list[str]) -> None:
    """
    Record which tickers have been mentioned in a session — the price ticker
    worker only polls tickers that are actually relevant to a room.
    """
    client = await getRedisClient()
    if not client:
        return
    activeSessions = await getActiveSessions()
    for session in activeSessions:
        if session["sessionId"] == sessionId:
            for ticker in tickers:
                if ticker not in session["mentionedTickers"]:
                    session["mentionedTickers"].append(ticker)

    await client.set(
        REDIS_KEY_ACTIVE_SESSIONS,
        json.dumps(activeSessions),
        ex=REDIS_ACTIVE_SESSION_TTL
    )

# ── Socket-to-user mapping (used for direct personal notifications, Phase 4+) ──

async def mapSocketToUser(userId: str, socketId: str) -> None:
    client = await getRedisClient()
    if not client:
        return
    await client.set(f"{REDIS_KEY_SOCKET_USER_MAP}:{userId}", socketId, ex=REDIS_SOCKET_MAP_TTL)

async def getSocketIdForUser(userId: str) -> str | None:
    client = await getRedisClient()
    if not client:
        return None
    return await client.get(f"{REDIS_KEY_SOCKET_USER_MAP}:{userId}")

async def removeSocketForUser(userId: str) -> None:
    client = await getRedisClient()
    if not client:
        return
    await client.delete(f"{REDIS_KEY_SOCKET_USER_MAP}:{userId}")

# ── Rate limiting ────────────────────────────────────────────────────────────────

async def incrementDailyQueryCount(userId: str) -> int:
    """
    Increment and return today's query count for a user.
    Key auto-expires at midnight (86400 seconds from first increment of the day).
    Returns 1 (always allowed) if Redis is not configured.
    """
    client = await getRedisClient()
    if not client:
        return 1    # no Redis → no rate limiting, always allow
    from datetime import datetime
    today    = datetime.utcnow().strftime("%Y-%m-%d")
    cacheKey = f"{RATE_LIMIT_KEY_PREFIX}:{userId}:{today}"

    count = await client.incr(cacheKey)
    if count == 1:
        await client.expire(cacheKey, 86400)
    return count
