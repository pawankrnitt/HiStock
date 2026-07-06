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
from repo.sessionRepo import insertSession, fetchSessionById, addMemberToSession
from repo.messageRepo import fetchSessionMessages

def registerSessionHandlers():

    @sio.on(SocketEventEnum.CREATE_SESSION)
    async def onCreateSession(sid, data):
        try:
            eventData = CreateSessionEventSchema(**data)
            session   = await sio.get_session(sid)
            sessionId = f"sess_{uuid.uuid4().hex[:12]}"

            await insertSession(sessionId, eventData.name, session["userId"])

            await handleJoinSessionInternal(sid, sessionId, session)

            await sio.emit("session_created", {
                "sessionId": sessionId,
                "name":      eventData.name
            }, to=sid)

        except ValidationError as e:
            await sio.emit(SocketEventEnum.ERROR, {"code": "INVALID_INPUT", "message": str(e)}, to=sid)

    @sio.on(SocketEventEnum.JOIN_SESSION)
    async def onJoinSession(sid, data):
        try:
            eventData = JoinSessionEventSchema(**data)

            existingSession = await fetchSessionById(eventData.sessionId)
            if not existingSession:
                await sio.emit(SocketEventEnum.ERROR, {
                    "code": "SESSION_NOT_FOUND", "message": "This session does not exist."
                }, to=sid)
                return

            session = await sio.get_session(sid)
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
    userId = session["userId"]
    name   = session.get("name", "User")

    await sio.enter_room(sid, sessionId)
    await addUserToActiveSession(sessionId, userId)
    await addMemberToSession(sessionId, userId)

    messageHistory = await fetchSessionMessages(sessionId)
    dbSession       = await fetchSessionById(sessionId)

    joinedPayload = SessionJoinedEventSchema(
        sessionId=sessionId,
        history=[m.model_dump() for m in messageHistory],
        members=dbSession.memberIds if dbSession else [userId]
    )
    await sio.emit(SocketEventEnum.SESSION_JOINED, joinedPayload.model_dump(), to=sid)

    await sio.emit(
        SocketEventEnum.USER_JOINED,
        UserPresenceEventSchema(userId=userId, name=name).model_dump(),
        room=sessionId,
        skip_sid=sid
    )
