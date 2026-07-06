from pydantic import BaseModel

class TriggerReportResponseSchema(BaseModel):
    success:   bool
    sessionId: str
    message:   str

class ReportUrlSchema(BaseModel):
    sessionId:   str
    downloadUrl: str | None
    status:      str    # "pending" | "ready" | "not_found"
