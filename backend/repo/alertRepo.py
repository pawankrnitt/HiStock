import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from db.dynamoDb import getTable
from schema.alertSchema import AlertSchema
from constant.appConstants import DYNAMODB_ALERTS_TABLE

async def insertAlert(userId: str, ticker: str, condition: str, value: float) -> AlertSchema:
    table = getTable(DYNAMODB_ALERTS_TABLE)
    alertData = {
        "alertId":     f"alert_{uuid.uuid4().hex[:12]}",
        "userId":      userId,
        "ticker":      ticker,
        "condition":   condition,
        "value":       value,
        "isActive":    True,
        "createdAt":   datetime.utcnow().isoformat(),
        "triggeredAt": None
    }
    table.put_item(Item=alertData)
    return AlertSchema(**alertData)

async def fetchAlertsByUser(userId: str) -> list[AlertSchema]:
    table    = getTable(DYNAMODB_ALERTS_TABLE)
    response = table.query(
        IndexName="userId-index",
        KeyConditionExpression=Key("userId").eq(userId)
    )
    return [AlertSchema(**item) for item in response.get("Items", [])]

async def fetchAlertById(alertId: str) -> AlertSchema | None:
    table    = getTable(DYNAMODB_ALERTS_TABLE)
    response = table.get_item(Key={"alertId": alertId})
    item     = response.get("Item")
    return AlertSchema(**item) if item else None

async def deleteAlert(alertId: str) -> None:
    table = getTable(DYNAMODB_ALERTS_TABLE)
    table.delete_item(Key={"alertId": alertId})
