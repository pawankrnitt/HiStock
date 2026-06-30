from pydantic import BaseModel

class SuccessSchema(BaseModel):
    success: bool = True
    message: str

class ErrorResponseSchema(BaseModel):
    success: bool  = False
    code:    str
    message: str
    detail:  str | None = None
