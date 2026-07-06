import uuid
from fastapi import HTTPException, status
from schema.documentSchema import (
    PresignUrlRequestSchema, PresignUrlResponseSchema, UserDocumentSchema
)
from schema.userSchema import UserSchema
from repo.userDocumentRepo import insertUserDocument, fetchUserDocuments, fetchUserDocumentById, deleteUserDocument
from service.s3Service import generatePresignUrl
from constant.appConstants import ALLOWED_UPLOAD_CONTENT_TYPES, S3_UPLOADS_PREFIX

async def getPresignUrl(
    body: PresignUrlRequestSchema, currentUser: UserSchema
) -> PresignUrlResponseSchema:
    if body.contentType not in ALLOWED_UPLOAD_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {body.contentType}"
        )

    docId = f"udoc_{uuid.uuid4().hex[:12]}"
    s3Key = f"{S3_UPLOADS_PREFIX}/{currentUser.userId}/{docId}/{body.fileName}"

    presignUrl = generatePresignUrl(s3Key, body.contentType)

    await insertUserDocument(docId, currentUser.userId, body.fileName, s3Key)

    return PresignUrlResponseSchema(presignUrl=presignUrl, docId=docId, s3Key=s3Key)

async def listUserDocuments(currentUser: UserSchema) -> list[UserDocumentSchema]:
    return await fetchUserDocuments(currentUser.userId)

async def removeUserDocument(docId: str, currentUser: UserSchema) -> None:
    document = await fetchUserDocumentById(docId)
    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    if document.userId != currentUser.userId:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your document")

    await deleteUserDocument(docId)
