from pydantic import BaseModel, Field
from enums.tickerEnum import TickerEnum

# ── Tool Input Schemas ────────────────────────────────────────────────────────

class StockPriceInputSchema(BaseModel):
    ticker:    TickerEnum
    startDate: str | None = None    # ISO date string "2024-01-01"
    endDate:   str | None = None

class SearchDocumentsInputSchema(BaseModel):
    query:   str = Field(..., min_length=3)
    company: TickerEnum | None = None    # None = search both

class SearchNewsInputSchema(BaseModel):
    company:  TickerEnum | None = None   # None = search both
    daysBack: int = Field(default=30, ge=1, le=90)

class CalculateRatioInputSchema(BaseModel):
    metric: str    # e.g. "pe_ratio", "gross_margin", "debt_to_equity"
    ticker: TickerEnum

# ── Tool Output Schemas ───────────────────────────────────────────────────────

class PricePointSchema(BaseModel):
    date:   str
    open:   float
    high:   float
    low:    float
    close:  float
    volume: int

class StockPriceOutputSchema(BaseModel):
    ticker:          str
    currentPrice:    float
    change:          float
    changePercent:   float
    historicalData:  list[PricePointSchema] | None = None
    error:           str | None = None

class NewsArticleSchema(BaseModel):
    title:       str
    description: str | None
    source:      str
    publishedAt: str
    url:         str

class SearchNewsOutputSchema(BaseModel):
    articles:     list[NewsArticleSchema]
    totalResults: int
    error:        str | None = None

class SearchDocumentsOutputSchema(BaseModel):
    chunks:     list[dict]    # ChunkSchema dicts (avoid circular import)
    totalFound: int
    error:      str | None = None

class RatioOutputSchema(BaseModel):
    metric:  str
    ticker:  str
    value:   float | None
    period:  str | None
    error:   str | None = None

# ── Agent-level Schemas ───────────────────────────────────────────────────────

class ToolCallSchema(BaseModel):
    toolName:   str
    inputData:  dict
    outputData: dict
    success:    bool
    calledAt:   str

class SubQuerySchema(BaseModel):
    query:   str
    company: str | None    # "NVDA" | "TSLA" | None
    tool:    str           # tool name to use

class AgentQuerySchema(BaseModel):
    question:  str = Field(..., min_length=5, max_length=1000)
    company:   TickerEnum | None = None
    sessionId: str | None = None    # None in Phase 2 — used from Phase 3

class AgentResponseSchema(BaseModel):
    answer:          str
    sources:         list[dict]
    toolCallHistory: list[ToolCallSchema]
    iterationCount:  int
    model:           str
    question:        str
