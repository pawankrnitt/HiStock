from pydantic import BaseModel, Field
from enums.tickerEnum import TickerEnum
from enums.alertConditionEnum import AlertConditionEnum

class CreateAlertSchema(BaseModel):
    ticker:    TickerEnum
    condition: AlertConditionEnum
    value:     float = Field(..., gt=0)

class AlertSchema(BaseModel):
    alertId:     str
    userId:      str
    ticker:      str
    condition:   str
    value:       float
    isActive:    bool
    createdAt:   str
    triggeredAt: str | None = None

class AlertResponseSchema(BaseModel):
    alertId:     str
    ticker:      str
    condition:   str
    value:       float
    isActive:    bool
    createdAt:   str
    triggeredAt: str | None
