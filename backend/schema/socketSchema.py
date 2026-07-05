# schema/socketSchema.py
from pydantic import BaseModel, Field

# ── Client → Server event payloads ────────────────────────────────────────────

class JoinSessionEventSchema(BaseModel):
    sessionId: str = Field(..., min_length=1)

class LeaveSessionEventSchema(BaseModel):
    sessionId: str

class CreateSessionEventSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class AskQuestionEventSchema(BaseModel):
    sessionId: str
    question:  str = Field(..., min_length=5, max_length=1000)
    messageId: str

class TypingStartEventSchema(BaseModel):
    sessionId: str

class TypingStopEventSchema(BaseModel):
    sessionId: str

# ── Server → Client event payloads ────────────────────────────────────────────

class SessionJoinedEventSchema(BaseModel):
    sessionId: str
    history:   list[dict]    # message dicts — empty in Phase 3, populated from Phase 4
    members:   list[str]

class UserPresenceEventSchema(BaseModel):
    userId: str
    name:   str

class QuestionReceivedEventSchema(BaseModel):
    question:  str
    askedBy:   str
    messageId: str

class AiThinkingEventSchema(BaseModel):
    step: str

class AiTokenEventSchema(BaseModel):
    token:     str
    messageId: str

class AiDoneEventSchema(BaseModel):
    messageId: str
    answer:    str
    sources:   list[dict]

class PriceUpdateEventSchema(BaseModel):
    ticker:        str
    price:         float
    change:        float
    changePercent: float

class RateLimitExceededEventSchema(BaseModel):
    message: str

class SocketErrorEventSchema(BaseModel):
    code:    str
    message: str
