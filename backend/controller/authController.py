from fastapi import HTTPException, status
from schema.userSchema import (
    SignupSchema, LoginSchema, RefreshTokenSchema,
    TokenResponseSchema, UserResponseSchema
)
from service.cognitoService import signupUser, loginUser, refreshAccessToken
from repo.userRepo import insertUser, fetchUserById
from constant.appConstants import ACCESS_TOKEN_EXPIRY_SECONDS

async def signup(body: SignupSchema) -> UserResponseSchema:
    try:
        userId = signupUser(body.email, body.password, body.name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    user = await insertUser(userId, body.email, body.name)
    return UserResponseSchema(userId=user.userId, email=user.email, name=user.name, plan=user.plan)

async def login(body: LoginSchema) -> TokenResponseSchema:
    try:
        authResult = loginUser(body.email, body.password)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    return TokenResponseSchema(
        accessToken=authResult["AccessToken"],
        refreshToken=authResult["RefreshToken"],
        expiresIn=authResult.get("ExpiresIn", ACCESS_TOKEN_EXPIRY_SECONDS)
    )

async def refresh(body: RefreshTokenSchema) -> TokenResponseSchema:
    try:
        authResult = refreshAccessToken(body.refreshToken)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    return TokenResponseSchema(
        accessToken=authResult["AccessToken"],
        refreshToken=body.refreshToken,
        expiresIn=authResult.get("ExpiresIn", ACCESS_TOKEN_EXPIRY_SECONDS)
    )
