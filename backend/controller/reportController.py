from fastapi import HTTPException, status
from schema.reportSchema import TriggerReportResponseSchema, ReportUrlSchema
from schema.userSchema import UserSchema
from repo.sessionRepo import fetchSessionById
from db.s3Client import getS3Client
from constant.appConstants import S3_REPORTS_BUCKET, REPORT_URL_EXPIRY_SECONDS

async def triggerReport(sessionId: str, currentUser: UserSchema) -> TriggerReportResponseSchema:
    session = await fetchSessionById(sessionId)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if currentUser.userId not in session.memberIds:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this session")

    return TriggerReportResponseSchema(
        success=True,
        sessionId=sessionId,
        message="Report generation requested. This will be available once Phase 6's Lambda pipeline is deployed."
    )

async def getReportUrl(sessionId: str, currentUser: UserSchema) -> ReportUrlSchema:
    session = await fetchSessionById(sessionId)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    s3Client = getS3Client()
    s3Key    = f"reports/{currentUser.userId}/{sessionId}.pdf"

    try:
        s3Client.head_object(Bucket=S3_REPORTS_BUCKET, Key=s3Key)
        downloadUrl = s3Client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_REPORTS_BUCKET, "Key": s3Key},
            ExpiresIn=REPORT_URL_EXPIRY_SECONDS
        )
        return ReportUrlSchema(sessionId=sessionId, downloadUrl=downloadUrl, status="ready")
    except Exception:
        return ReportUrlSchema(sessionId=sessionId, downloadUrl=None, status="pending")
