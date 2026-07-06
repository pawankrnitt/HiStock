from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from service.cognitoService import verifyAccessToken
from repo.userRepo import fetchUserById
from schema.userSchema import UserSchema

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

async def getCurrentUser(token: str = Depends(oauth2Scheme)) -> UserSchema:
    try:
        claims = await verifyAccessToken(token)
        userId = claims["sub"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = await fetchUserById(userId)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
