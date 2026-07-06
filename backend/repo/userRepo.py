from datetime import datetime
from db.dynamoDb import getTable
from schema.userSchema import UserSchema
from constant.appConstants import DYNAMODB_USERS_TABLE

async def insertUser(userId: str, email: str, name: str) -> UserSchema:
    table    = getTable(DYNAMODB_USERS_TABLE)
    userData = {
        "userId":          userId,
        "email":           email,
        "name":            name,
        "plan":            "free",
        "createdAt":       datetime.utcnow().isoformat(),
        "watchlist":       [],
        "dailyQueryCount": 0,
        "lastQueryDate":   None
    }
    table.put_item(Item=userData)
    return UserSchema(**userData)

async def fetchUserById(userId: str) -> UserSchema | None:
    table    = getTable(DYNAMODB_USERS_TABLE)
    response = table.get_item(Key={"userId": userId})
    item     = response.get("Item")
    return UserSchema(**item) if item else None
