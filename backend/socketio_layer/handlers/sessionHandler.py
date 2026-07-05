# socketio_layer/handlers/sessionHandler.py
# Responsibility: Session lifecycle events — create, join, leave.
# Phase 3 keeps session membership in Redis only (no DynamoDB yet — Phase 4 adds
# persistent storage; this file's function signatures don't change in Phase 4,
# only the internals get a DynamoDB write/read added alongside Redis).

import uuid
from pydantic import ValidationError
from socketio_layer.socketServer import sio
from schema.socketSchema import (
    JoinSessionEventSchema, LeaveSessionEventSchema,
    CreateSessionEventSchema, SessionJoinedEventSchema,
    UserPresenceEventSchema
)
from enums.socketEventEnum import SocketEventEnum
from service.redisService import addUserToActiveSession, removeUserFromActiveSession

def registerSessionHandlers():
    """Register all session-related Socket.io event handlers."""

    @sio.on(SocketEventEnum.CREATE_SESSION)
    async def onCreateSession(sid, data):
        try:
            eventData = CreateSessionEventSchema(**data)
            session   = await sio.get_session(sid)
            sessionId = f"sess_{uuid.uuid4().hex[:12]}"

            await handleJoinSessionInternal(sid, sessionId, session)

            await sio.emit(SocketEventEnum.SESSION_CREATED, {
                "sessionId": sessionId,
                "name":      eventData.name
            }, to=sid)

        except ValidationError as e:
            await sio.emit(SocketEventEnum.ERROR, {"code": "INVALID_INPUT", "message": str(e)}, to=sid)

    @sio.on(SocketEventEnum.JOIN_SESSION)
    async def onJoinSession(sid, data):
        try:
            eventData = JoinSessionEventSchema(**data)
            session   = await sio.get_session(sid)
            await handleJoinSessionInternal(sid, eventData.sessionId, session)

        except ValidationError as e:
            await sio.emit(SocketEventEnum.ERROR, {"code": "INVALID_INPUT", "message": str(e)}, to=sid)

    @sio.on(SocketEventEnum.LEAVE_SESSION)
    async def onLeaveSession(sid, data):
        try:
            eventData = LeaveSessionEventSchema(**data)
            session   = await sio.get_session(sid)
            userId    = session["userId"]

            await sio.leave_room(sid, eventData.sessionId)
            await removeUserFromActiveSession(eventData.sessionId, userId)

            await sio.emit(
                SocketEventEnum.USER_LEFT,
                UserPresenceEventSchema(userId=userId, name=session.get("name", "User")).model_dump(),
                room=eventData.sessionId
            )

        except ValidationError as e:
            await sio.emit(SocketEventEnum.ERROR, {"code": "INVALID_INPUT", "message": str(e)}, to=sid)

async def handleJoinSessionInternal(sid: str, sessionId: str, session: dict) -> None:
    """
    Shared logic for both create_session and join_session — joins the Socket.io
    room, tracks the user in Redis active sessions, and notifies the room.
    """
    userId = session["userId"]
    name   = session.get("name", "User")

    await sio.enter_room(sid, sessionId)
    await addUserToActiveSession(sessionId, userId)

    # Phase 3: history is always empty (no persistence yet) — Phase 4 fetches
    # real message history from DynamoDB here instead of an empty list.
    joinedPayload = SessionJoinedEventSchema(
        sessionId=sessionId,
        history=[],
        members=[userId]
    )
    await sio.emit(SocketEventEnum.SESSION_JOINED, joinedPayload.model_dump(), to=sid)

    await sio.emit(
        SocketEventEnum.USER_JOINED,
        UserPresenceEventSchema(userId=userId, name=name).model_dump(),
        room=sessionId,
        skip_sid=sid
    )
