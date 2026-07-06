import uuid
from fastapi import HTTPException, status
from schema.sessionSchema import CreateSessionSchema, SessionResponseSchema, SessionWithHistorySchema
from schema.userSchema import UserSchema
from repo.sessionRepo import insertSession, fetchSessionById, fetchSessionsByUser, deleteSession
from repo.messageRepo import fetchSessionMessages

async def createSession(body: CreateSessionSchema, currentUser: UserSchema) -> SessionResponseSchema:
    sessionId = f"sess_{uuid.uuid4().hex[:12]}"
    session   = await insertSession(sessionId, body.name, currentUser.userId)
    return SessionResponseSchema(**session.model_dump())

async def listUserSessions(currentUser: UserSchema) -> list[SessionResponseSchema]:
    sessions = await fetchSessionsByUser(currentUser.userId)
    return [SessionResponseSchema(**s.model_dump()) for s in sessions]

async def getSessionWithHistory(sessionId: str, currentUser: UserSchema) -> SessionWithHistorySchema:
    session = await fetchSessionById(sessionId)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    if currentUser.userId not in session.memberIds:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this session")

    messages = await fetchSessionMessages(sessionId)
    return SessionWithHistorySchema(
        **session.model_dump(),
        messages=[m.model_dump() for m in messages]
    )

async def removeSession(sessionId: str, currentUser: UserSchema) -> None:
    session = await fetchSessionById(sessionId)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    if session.creatorId != currentUser.userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the creator can delete a session")

    await deleteSession(sessionId)
