from pydantic import BaseModel, Field

class CreateSessionSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class SessionSchema(BaseModel):
    sessionId:         str
    name:              str
    creatorId:         str
    memberIds:         list[str]
    mentionedTickers:  list[str] = []
    isPublic:          bool = False
    createdAt:         str
    lastActiveAt:      str

class SessionResponseSchema(BaseModel):
    sessionId:         str
    name:              str
    creatorId:         str
    memberIds:         list[str]
    mentionedTickers:  list[str]
    createdAt:         str
    lastActiveAt:      str

class SessionWithHistorySchema(SessionResponseSchema):
    messages: list[dict]    # MessageSchema dicts — avoids circular import
