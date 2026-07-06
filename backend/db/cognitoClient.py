import boto3
from constant.appConstants import COGNITO_REGION

_cognitoClient = None

def getCognitoClient():
    global _cognitoClient
    if _cognitoClient is None:
        _cognitoClient = boto3.client("cognito-idp", region_name=COGNITO_REGION)
    return _cognitoClient
