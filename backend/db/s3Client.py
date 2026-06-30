import boto3
from constant.appConstants import AWS_REGION

_s3Client = None

def getS3Client():
    global _s3Client
    if _s3Client is None:
        _s3Client = boto3.client("s3", region_name=AWS_REGION)
    return _s3Client
