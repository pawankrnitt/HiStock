from pydantic import BaseModel, Field
from enums.tickerEnum import TickerEnum

class RagQuerySchema(BaseModel):
    question: str     = Field(..., min_length=5, max_length=1000)
    company:  TickerEnum | None = None    # None = search both NVDA and TSLA

class SourceSchema(BaseModel):
    doc:       str
    section:   str
    company:   str
    docType:   str
    date:      str
    page:      int | None  = None
    score:     float

class ChunkSchema(BaseModel):
    text:      str
    source:    str
    section:   str
    company:   str
    docType:   str
    date:      str
    namespace: str
    score:     float | None = None

class RetrievalResultSchema(BaseModel):
    chunks:     list[ChunkSchema]
    totalFound: int

class RagResponseSchema(BaseModel):
    answer:  str
    sources: list[SourceSchema]
    model:   str
    question: str
