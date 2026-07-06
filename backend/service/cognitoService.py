import httpx
from jose import jwk, jwt
from jose.utils import base64url_decode
from db.cognitoClient import getCognitoClient
from constant.appConstants import (
    COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID, COGNITO_JWKS_URL, JWT_ALGORITHM
)

_jwksCache = None

async def getJwks() -> dict:
    global _jwksCache
    if _jwksCache is None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(COGNITO_JWKS_URL)
            response.raise_for_status()
            _jwksCache = response.json()
    return _jwksCache

async def verifyAccessToken(token: str) -> dict:
    jwks    = await getJwks()
    headers = jwt.get_unverified_headers(token)
    kid     = headers["kid"]

    matchingKey = next((key for key in jwks["keys"] if key["kid"] == kid), None)
    if not matchingKey:
        raise ValueError("Public key not found in JWKS for this token")

    publicKey = jwk.construct(matchingKey)
    message, encodedSignature = token.rsplit(".", 1)
    decodedSignature = base64url_decode(encodedSignature.encode())

    if not publicKey.verify(message.encode(), decodedSignature):
        raise ValueError("Token signature verification failed")

    claims = jwt.get_unverified_claims(token)
    return claims

def signupUser(email: str, password: str, name: str) -> str:
    client = getCognitoClient()
    response = client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=email,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "name",  "Value": name},
            {"Name": "custom:plan", "Value": "free"}
        ]
    )
    client.admin_confirm_sign_up(UserPoolId=COGNITO_USER_POOL_ID, Username=email)
    return response["UserSub"]

def loginUser(email: str, password: str) -> dict:
    client   = getCognitoClient()
    response = client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": email, "PASSWORD": password}
    )
    return response["AuthenticationResult"]

def refreshAccessToken(refreshToken: str) -> dict:
    client   = getCognitoClient()
    response = client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": refreshToken}
    )
    return response["AuthenticationResult"]
