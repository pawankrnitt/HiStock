# socketio_layer/middleware/rateLimitMiddleware.py
# Responsibility: Check whether a user has exceeded their daily query limit
# before the agent graph is invoked. Called explicitly inside questionHandler —
# NOT a Socket.io middleware decorator, since it only applies to ask_question.

from service.redisService import incrementDailyQueryCount
from constant.appConstants import DAILY_FREE_QUERY_LIMIT, DAILY_PRO_QUERY_LIMIT

async def checkRateLimit(userId: str, userPlan: str) -> bool:
    """
    Increment today's query count and check against the plan's daily limit.
    Returns True if the request is allowed, False if the limit is exceeded.
    """
    currentCount = await incrementDailyQueryCount(userId)
    limit        = DAILY_PRO_QUERY_LIMIT if userPlan == "pro" else DAILY_FREE_QUERY_LIMIT
    return currentCount <= limit
