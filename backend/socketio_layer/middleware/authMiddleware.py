from socketio_layer.socketServer import sio
from service.cognitoService import verifyAccessToken
from service.redisService import mapSocketToUser
from repo.userRepo import fetchUserById

def registerAuthMiddleware():
    """Register the connect handler — now with real JWT verification."""

    @sio.event
    async def connect(sid, environ, auth):
        token = auth.get("token") if auth else None

        if not token:
            raise ConnectionRefusedError("authentication_failed")

        try:
            claims = await verifyAccessToken(token)
            userId = claims["sub"]
        except Exception:
            raise ConnectionRefusedError("invalid_token")

        user = await fetchUserById(userId)
        if not user:
            raise ConnectionRefusedError("user_not_found")

        await sio.save_session(sid, {
            "userId": user.userId,
            "name":   user.name,
            "plan":   user.plan.value
        })

        await mapSocketToUser(user.userId, sid)
        print(f"[socket] connected: sid={sid} userId={user.userId}")
