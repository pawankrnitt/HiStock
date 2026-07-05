# socketio_layer/middleware/authMiddleware.py
# Responsibility: Verify the connecting client on the Socket.io "connect" event.
#
# PHASE 3 NOTE: Real Cognito JWT verification is built in Phase 4 alongside the
# REST auth endpoints. Phase 3 uses a stubbed check so Socket.io plumbing can be
# built and tested independently of the auth system. The function signature and
# session shape stay identical — Phase 4 only swaps the verification logic inside.

from socketio_layer.socketServer import sio
from service.redisService import mapSocketToUser

def registerAuthMiddleware():
    """Register the connect handler that gatekeeps every Socket.io connection."""

    @sio.event
    async def connect(sid, environ, auth):
        token = auth.get("token") if auth else None

        if not token:
            raise ConnectionRefusedError("authentication_failed")

        # ── PHASE 3 STUB ──────────────────────────────────────────────────────
        # Accepts any non-empty token and derives a fake userId from it.
        # Phase 4 replaces this block with real jwt.decode() against Cognito's
        # public key, raising ConnectionRefusedError("invalid_token") on failure.
        userId   = f"user_{token[:8]}"
        userName = f"Guest-{token[:4]}"
        userPlan = "free"
        # ──────────────────────────────────────────────────────────────────────

        await sio.save_session(sid, {
            "userId":   userId,
            "name":     userName,
            "plan":     userPlan
        })

        await mapSocketToUser(userId, sid)

        print(f"[socket] connected: sid={sid} userId={userId}")
