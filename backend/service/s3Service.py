from db.s3Client import getS3Client
from constant.appConstants import S3_DOCUMENTS_BUCKET, S3_DOCUMENTS_PREFIX

def uploadRawDocument(fileBytes: bytes, s3Key: str) -> str:
    client = getS3Client()
    client.put_object(Bucket=S3_DOCUMENTS_BUCKET, Key=s3Key, Body=fileBytes)
    return s3Key

def downloadDocument(s3Key: str) -> bytes:
    client   = getS3Client()
    response = client.get_object(Bucket=S3_DOCUMENTS_BUCKET, Key=s3Key)
    return response["Body"].read()

from constant.appConstants import S3_UPLOADS_BUCKET, PRESIGN_URL_EXPIRY_SECONDS

def generatePresignUrl(s3Key: str, contentType: str) -> str:
    """
    Generate a pre-signed S3 PUT URL — the frontend uploads directly to S3
    using this URL, bypassing the backend entirely for the file bytes.
    """
    client = getS3Client()
    return client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket":      S3_UPLOADS_BUCKET,
            "Key":         s3Key,
            "ContentType": contentType
        },
        ExpiresIn=PRESIGN_URL_EXPIRY_SECONDS
    )
