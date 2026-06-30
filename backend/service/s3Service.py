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
