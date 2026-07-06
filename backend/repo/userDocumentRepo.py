from datetime import datetime
from boto3.dynamodb.conditions import Key
from db.dynamoDb import getTable
from schema.documentSchema import UserDocumentSchema
from constant.appConstants import DYNAMODB_USER_DOCS_TABLE

async def insertUserDocument(
    docId: str, userId: str, fileName: str, s3Key: str
) -> UserDocumentSchema:
    table = getTable(DYNAMODB_USER_DOCS_TABLE)
    docData = {
        "docId":       docId,
        "userId":      userId,
        "fileName":    fileName,
        "s3Key":       s3Key,
        "namespace":   f"user_{userId}",
        "chunksCount": 0,
        "status":      "pending",
        "uploadedAt":  datetime.utcnow().isoformat()
    }
    table.put_item(Item=docData)
    return UserDocumentSchema(**docData)

async def fetchUserDocuments(userId: str) -> list[UserDocumentSchema]:
    table    = getTable(DYNAMODB_USER_DOCS_TABLE)
    response = table.query(
        IndexName="userId-index",
        KeyConditionExpression=Key("userId").eq(userId)
    )
    return [UserDocumentSchema(**item) for item in response.get("Items", [])]

async def fetchUserDocumentById(docId: str) -> UserDocumentSchema | None:
    table    = getTable(DYNAMODB_USER_DOCS_TABLE)
    response = table.get_item(Key={"docId": docId})
    item     = response.get("Item")
    return UserDocumentSchema(**item) if item else None

async def deleteUserDocument(docId: str) -> None:
    table = getTable(DYNAMODB_USER_DOCS_TABLE)
    table.delete_item(Key={"docId": docId})
