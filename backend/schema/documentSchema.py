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

class PresignUrlRequestSchema(BaseModel):
    fileName:    str = Field(..., min_length=1)
    contentType: str

class PresignUrlResponseSchema(BaseModel):
    presignUrl: str
    docId:      str
    s3Key:      str

class UserDocumentSchema(BaseModel):
    docId:       str
    userId:      str
    fileName:    str
    s3Key:       str
    namespace:   str
    chunksCount: int = 0
    status:      str    # "pending" | "processing" | "completed" | "failed"
    uploadedAt:  str
