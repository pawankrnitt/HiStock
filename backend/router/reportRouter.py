from fastapi import APIRouter, Depends
from controller.reportController import triggerReport, getReportUrl
from schema.reportSchema import TriggerReportResponseSchema, ReportUrlSchema
from schema.userSchema import UserSchema
from middleware.authMiddleware import getCurrentUser

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/{sessionId}", response_model=TriggerReportResponseSchema)
async def triggerReportRoute(
    sessionId: str,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> TriggerReportResponseSchema:
    return await triggerReport(sessionId, currentUser)

@router.get("/{sessionId}", response_model=ReportUrlSchema)
async def getReportRoute(
    sessionId: str,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> ReportUrlSchema:
    return await getReportUrl(sessionId, currentUser)
