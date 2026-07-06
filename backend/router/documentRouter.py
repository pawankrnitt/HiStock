from fastapi import APIRouter, Depends, status
from controller.documentController import getPresignUrl, listUserDocuments, removeUserDocument
from schema.documentSchema import PresignUrlRequestSchema, PresignUrlResponseSchema, UserDocumentSchema
from schema.userSchema import UserSchema
from middleware.authMiddleware import getCurrentUser

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/presign", response_model=PresignUrlResponseSchema)
async def getPresignUrlRoute(
    body: PresignUrlRequestSchema,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> PresignUrlResponseSchema:
    return await getPresignUrl(body, currentUser)

@router.get("/", response_model=list[UserDocumentSchema])
async def listDocumentsRoute(
    currentUser: UserSchema = Depends(getCurrentUser)
) -> list[UserDocumentSchema]:
    return await listUserDocuments(currentUser)

@router.delete("/{docId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteDocumentRoute(
    docId: str,
    currentUser: UserSchema = Depends(getCurrentUser)
) -> None:
    await removeUserDocument(docId, currentUser)
