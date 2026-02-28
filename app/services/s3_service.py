import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile
import uuid
from core.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
    AWS_S3_REGION_NAME
)

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_S3_REGION_NAME
    )

async def upload_image_to_s3(file: UploadFile) -> str:
    """Upload image to S3 and return the image_key (filename)"""
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        print("AWS Credentials not set, skipping S3 upload")
        return f"dev_mock_{uuid.uuid4()}_{file.filename}"

    s3 = get_s3_client()
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    
    try:
        s3.upload_fileobj(
            file.file,
            AWS_STORAGE_BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": file.content_type}
        )
        return unique_filename
    except NoCredentialsError:
        print("Credentials not available")
        return f"error_{unique_filename}"
    except Exception as e:
        print(f"S3 Upload failed: {e}")
        return f"failed_{unique_filename}"

def generate_presigned_url(image_key: str, expiration: int = 3600) -> str:
    """Generate a pre-signed URL for an S3 object"""
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        # Mock URL for development
        return f"https://mock-s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/{image_key}?token=mock"

    s3 = get_s3_client()
    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': AWS_STORAGE_BUCKET_NAME, 'Key': image_key},
            ExpiresIn=expiration
        )
        return response
    except Exception as e:
        print(f"Failed to generate pre-signed URL: {e}")
        return ""
