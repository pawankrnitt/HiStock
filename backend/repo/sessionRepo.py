from datetime import datetime
from db.dynamoDb import getTable
from schema.sessionSchema import SessionSchema
from constant.appConstants import DYNAMODB_SESSIONS_TABLE

async def insertSession(sessionId: str, name: str, creatorId: str) -> SessionSchema:
    table = getTable(DYNAMODB_SESSIONS_TABLE)
    now   = datetime.utcnow().isoformat()
    sessionData = {
        "sessionId":        sessionId,
        "name":             name,
        "creatorId":        creatorId,
        "memberIds":        [creatorId],
        "mentionedTickers": [],
        "isPublic":         False,
        "createdAt":        now,
        "lastActiveAt":     now
    }
    table.put_item(Item=sessionData)
    return SessionSchema(**sessionData)

async def fetchSessionById(sessionId: str) -> SessionSchema | None:
    table    = getTable(DYNAMODB_SESSIONS_TABLE)
    response = table.get_item(Key={"sessionId": sessionId})
    item     = response.get("Item")
    return SessionSchema(**item) if item else None

async def fetchSessionsByUser(userId: str) -> list[SessionSchema]:
    table    = getTable(DYNAMODB_SESSIONS_TABLE)
    response = table.scan()
    items    = response.get("Items", [])
    userSessions = [SessionSchema(**item) for item in items if userId in item.get("memberIds", [])]
    return userSessions

async def addMemberToSession(sessionId: str, userId: str) -> None:
    table   = getTable(DYNAMODB_SESSIONS_TABLE)
    session = await fetchSessionById(sessionId)
    if session and userId not in session.memberIds:
        table.update_item(
            Key={"sessionId": sessionId},
            UpdateExpression="SET memberIds = list_append(memberIds, :newMember), lastActiveAt = :now",
            ExpressionAttributeValues={
                ":newMember": [userId],
                ":now": datetime.utcnow().isoformat()
            }
        )

async def addTickersToSessionRecord(sessionId: str, tickers: list[str]) -> None:
    session = await fetchSessionById(sessionId)
    if not session:
        return
    updatedTickers = list(set(session.mentionedTickers + tickers))
    table = getTable(DYNAMODB_SESSIONS_TABLE)
    table.update_item(
        Key={"sessionId": sessionId},
        UpdateExpression="SET mentionedTickers = :tickers, lastActiveAt = :now",
        ExpressionAttributeValues={
            ":tickers": updatedTickers,
            ":now": datetime.utcnow().isoformat()
        }
    )

async def deleteSession(sessionId: str) -> None:
    table = getTable(DYNAMODB_SESSIONS_TABLE)
    table.delete_item(Key={"sessionId": sessionId})
