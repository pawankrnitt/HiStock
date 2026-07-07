from pydantic import BaseModel, EmailStr, Field
from enums.userPlanEnum import UserPlanEnum

class SignupSchema(BaseModel):
    email:    EmailStr
    password: str = Field(..., min_length=8)
    name:     str = Field(..., min_length=1, max_length=100)

class LoginSchema(BaseModel):
    email:    EmailStr
    password: str

class RefreshTokenSchema(BaseModel):
    refreshToken: str

class TokenResponseSchema(BaseModel):
    accessToken:  str
    refreshToken: str
    expiresIn:    int
    tokenType:    str = "Bearer"

class UserSchema(BaseModel):
    userId:           str
    email:            str
    name:             str
    plan:             UserPlanEnum = UserPlanEnum.FREE
    createdAt:        str
    watchlist:        list[str] = []
    dailyQueryCount:  int = 0
    lastQueryDate:    str | None = None

class UserResponseSchema(BaseModel):
    userId: str
    email:  str
    name:   str
    plan:   UserPlanEnum = UserPlanEnum.FREE
