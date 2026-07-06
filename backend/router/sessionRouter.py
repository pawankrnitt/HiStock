from fastapi import APIRouter, Depends, status
from controller.sessionController import createSession, listUserSessions, getSessionWithHistory, removeSession
from schema.sessionSchema import CreateSessionSchema, SessionResponseSchema, SessionWithHistorySchema
from schema.userSchema import UserSchema
from middleware.authMiddleware import getCurrentUser

router = APIRouter(prefix="/sessions", tags=["sessions"])

@router.post("/", response_model=SessionResponseSchema, status_code=status.HTTP_201_CREATED)
async def createSessionRoute(
    body: CreateSessionSchema,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> SessionResponseSchema:
    return await createSession(body, currentUser)

@router.get("/", response_model=list[SessionResponseSchema])
async def listSessionsRoute(
    currentUser: UserSchema = Depends(getCurrentUser)
) -> list[SessionResponseSchema]:
    return await listUserSessions(currentUser)

@router.get("/{sessionId}", response_model=SessionWithHistorySchema)
async def getSessionRoute(
    sessionId: str,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> SessionWithHistorySchema:
    return await getSessionWithHistory(sessionId, currentUser)

@router.delete("/{sessionId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteSessionRoute(
    sessionId: str,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> None:
    await removeSession(sessionId, currentUser)
