import boto3
from constant.appConstants import AWS_REGION

_dynamoResource = None

def getDynamoClient():
    global _dynamoResource
    if _dynamoResource is None:
        _dynamoResource = boto3.resource("dynamodb", region_name=AWS_REGION)
    return _dynamoResource

def getTable(tableName: str):
    return getDynamoClient().Table(tableName)
