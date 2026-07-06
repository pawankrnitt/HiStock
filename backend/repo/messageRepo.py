import uuid
from datetime import datetime
from boto3.dynamodb.conditions import Key
from db.dynamoDb import getTable
from schema.messageSchema import MessageSchema
from constant.appConstants import DYNAMODB_MESSAGES_TABLE

async def insertMessage(
    sessionId: str,
    userId:    str,
    question:  str,
    answer:    str,
    sources:   list[dict]
) -> MessageSchema:
    table = getTable(DYNAMODB_MESSAGES_TABLE)
    messageData = {
        "messageId": f"msg_{uuid.uuid4().hex[:12]}",
        "sessionId": sessionId,
        "userId":    userId,
        "question":  question,
        "answer":    answer,
        "sources":   sources,
        "timestamp": datetime.utcnow().isoformat()
    }
    table.put_item(Item=messageData)
    return MessageSchema(**messageData)

async def fetchSessionMessages(sessionId: str) -> list[MessageSchema]:
    table    = getTable(DYNAMODB_MESSAGES_TABLE)
    response = table.query(
        IndexName="sessionId-index",
        KeyConditionExpression=Key("sessionId").eq(sessionId)
    )
    items = response.get("Items", [])
    items.sort(key=lambda m: m["timestamp"])
    return [MessageSchema(**item) for item in items]
