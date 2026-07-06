from fastapi import APIRouter, Depends, status
from controller.alertController import createAlert, listUserAlerts, removeAlert
from schema.alertSchema import CreateAlertSchema, AlertResponseSchema
from schema.userSchema import UserSchema
from middleware.authMiddleware import getCurrentUser

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/", response_model=AlertResponseSchema, status_code=status.HTTP_201_CREATED)
async def createAlertRoute(
    body: CreateAlertSchema,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> AlertResponseSchema:
    return await createAlert(body, currentUser)

@router.get("/", response_model=list[AlertResponseSchema])
async def listAlertsRoute(
    currentUser: UserSchema = Depends(getCurrentUser)
) -> list[AlertResponseSchema]:
    return await listUserAlerts(currentUser)

@router.delete("/{alertId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteAlertRoute(
    alertId: str,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> None:
    await removeAlert(alertId, currentUser)
