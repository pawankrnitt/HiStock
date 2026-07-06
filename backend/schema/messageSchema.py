from pydantic import BaseModel

class SourceReferenceSchema(BaseModel):
    type:    str            # "document" | "news"
    doc:     str
    section: str | None = None
    company: str | None = None
    date:    str | None = None
    score:   float | None = None

class MessageSchema(BaseModel):
    messageId:  str
    sessionId:  str
    userId:     str
    question:   str
    answer:     str
    sources:    list[SourceReferenceSchema]
    timestamp:  str
    tokensUsed: int | None = None
