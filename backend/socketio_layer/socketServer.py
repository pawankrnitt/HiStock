# socketio_layer/socketServer.py
# Responsibility: Create the Socket.io AsyncServer instance with the Redis
# pub/sub adapter attached. This is the ONLY file that constructs `sio`.
# Every handler file imports `sio` from here — never creates its own instance.
#
# Falls back to in-memory mode if UPSTASH_REDIS_URL is not configured —
# useful for local development before Redis is set up.

import socketio
from constant.appConstants import UPSTASH_REDIS_URL, SOCKET_REDIS_CHANNEL

# AsyncRedisManager turns Redis into a pub/sub broker between server instances.
# Without this, emitting to a room only reaches users connected to THIS process —
# a hard requirement once Phase 7 runs multiple ECS Fargate tasks behind an ALB.
if UPSTASH_REDIS_URL:
    from socketio import AsyncRedisManager
    clientManager = AsyncRedisManager(
        url=UPSTASH_REDIS_URL,
        channel=SOCKET_REDIS_CHANNEL
    )
    print(f"[socket] Using Redis pub/sub adapter (channel: {SOCKET_REDIS_CHANNEL})")
else:
    clientManager = None
    print("[socket] WARNING: UPSTASH_REDIS_URL not set — running in single-instance mode (no pub/sub)")

sio = socketio.AsyncServer(
    async_mode="asgi",
    client_manager=clientManager,
    cors_allowed_origins="*"          # tighten to frontend origin in Phase 7 deployment
)
