from fastapi import HTTPException, status
from schema.alertSchema import CreateAlertSchema, AlertResponseSchema
from schema.userSchema import UserSchema
from repo.alertRepo import insertAlert, fetchAlertsByUser, fetchAlertById, deleteAlert

async def createAlert(body: CreateAlertSchema, currentUser: UserSchema) -> AlertResponseSchema:
    alert = await insertAlert(
        userId=currentUser.userId,
        ticker=body.ticker.value,
        condition=body.condition.value,
        value=body.value
    )
    return AlertResponseSchema(**alert.model_dump())

async def listUserAlerts(currentUser: UserSchema) -> list[AlertResponseSchema]:
    alerts = await fetchAlertsByUser(currentUser.userId)
    return [AlertResponseSchema(**a.model_dump()) for a in alerts]

async def removeAlert(alertId: str, currentUser: UserSchema) -> None:
    alert = await fetchAlertById(alertId)
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    if alert.userId != currentUser.userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your alert")
    await deleteAlert(alertId)
