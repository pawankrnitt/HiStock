# socketio_layer/handlers/presenceHandler.py
# Responsibility: Typing indicators and disconnect cleanup.

from pydantic import ValidationError
from socketio_layer.socketServer import sio
from schema.socketSchema import TypingStartEventSchema, TypingStopEventSchema, UserPresenceEventSchema
from enums.socketEventEnum import SocketEventEnum
from service.redisService import removeUserFromActiveSession, removeSocketForUser, getActiveSessions

def registerPresenceHandlers():
    """Register typing indicator and disconnect handlers."""

    @sio.on(SocketEventEnum.TYPING_START)
    async def onTypingStart(sid, data):
        try:
            eventData = TypingStartEventSchema(**data)
            session   = await sio.get_session(sid)
            await sio.emit(
                SocketEventEnum.USER_TYPING,
                UserPresenceEventSchema(userId=session["userId"], name=session.get("name", "User")).model_dump(),
                room=eventData.sessionId,
                skip_sid=sid
            )
        except ValidationError:
            pass    # typing indicators are best-effort — silently ignore bad payloads

    @sio.on(SocketEventEnum.TYPING_STOP)
    async def onTypingStop(sid, data):
        try:
            eventData = TypingStopEventSchema(**data)
            session   = await sio.get_session(sid)
            await sio.emit(
                SocketEventEnum.USER_STOPPED_TYPING,
                {"userId": session["userId"]},
                room=eventData.sessionId,
                skip_sid=sid
            )
        except ValidationError:
            pass

    @sio.event
    async def disconnect(sid):
        session = await sio.get_session(sid)
        userId  = session.get("userId")

        if not userId:
            return

        # Find which active sessions this user belonged to, remove them from each
        activeSessions = await getActiveSessions()
        for activeSession in activeSessions:
            if userId in activeSession.get("memberIds", []):
                sessionId = activeSession["sessionId"]
                await removeUserFromActiveSession(sessionId, userId)

                # Notify remaining members the user has left
                await sio.emit(
                    SocketEventEnum.USER_LEFT,
                    UserPresenceEventSchema(userId=userId, name=session.get("name", "User")).model_dump(),
                    room=sessionId
                )

        # Clean up socket-to-user mapping
        await removeSocketForUser(userId)
        print(f"[socket] disconnected: sid={sid} userId={userId}")
