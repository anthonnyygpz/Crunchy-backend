from botocore.exceptions import ClientError
from fastapi import HTTPException
from botocore.config import Config
import boto3
import os

from app.utils.logger_AWS.logger import logger


def get_bucket_region(bucket_name):
    s3_client = boto3.client("s3")
    try:
        location = s3_client.get_bucket_location(Bucket=bucket_name)
        return location["LocationConstraint"] or "us-east-1"
    except ClientError as e:
        logger.error(f"Error al obtener la región del bucket: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error al obtener la región del bucket"
        )


bucket_name = os.getenv("S3_BUCKET_NAME")
region = get_bucket_region(bucket_name)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=region,
    config=Config(signature_version="s3v4"),
)
