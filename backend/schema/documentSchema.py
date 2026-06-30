from pydantic import BaseModel, Field
from enums.tickerEnum import TickerEnum
from enums.docTypeEnum import DocTypeEnum

class IngestionMetadataSchema(BaseModel):
    company:   TickerEnum
    docType:   DocTypeEnum
    period:    str              # e.g. "Q3-2024", "FY2024"
    url:       str
    namespace: str = "public"

class ProcessedDocSchema(BaseModel):
    docId:       str
    company:     str
    docType:     str
    period:      str
    s3Key:       str
    namespace:   str
    chunksCount: int
    status:      str            # "completed" | "failed"
    processedAt: str
