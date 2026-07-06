from fastapi import APIRouter, status
from controller.authController import signup, login, refresh
from schema.userSchema import (
    SignupSchema, LoginSchema, RefreshTokenSchema,
    TokenResponseSchema, UserResponseSchema
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def signupRoute(body: SignupSchema) -> UserResponseSchema:
    return await signup(body)

@router.post("/login", response_model=TokenResponseSchema)
async def loginRoute(body: LoginSchema) -> TokenResponseSchema:
    return await login(body)

@router.post("/refresh", response_model=TokenResponseSchema)
async def refreshRoute(body: RefreshTokenSchema) -> TokenResponseSchema:
    return await refresh(body)
