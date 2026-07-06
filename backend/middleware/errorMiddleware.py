from fastapi import Request
from fastapi.responses import JSONResponse
from schema.commonSchema import ErrorResponseSchema

async def globalExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
    errorBody = ErrorResponseSchema(
        code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred.",
        detail=str(exc)
    )
    return JSONResponse(status_code=500, content=errorBody.model_dump())
