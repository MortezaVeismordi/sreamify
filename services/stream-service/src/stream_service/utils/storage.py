import os
import boto3
from django.conf import settings
from typing import Optional


def upload_file(file_path: str, destination: str) -> Optional[str]:
    """
    Upload file to storage (S3 or local).
    Returns file URL or None if upload fails.
    """
    if settings.USE_LOCAL_STORAGE:
        return _upload_local(file_path, destination)
    else:
        return _upload_s3(file_path, destination)


def _upload_local(file_path: str, destination: str) -> str:
    """Upload file to local storage."""
    media_root = settings.MEDIA_ROOT
    dest_path = os.path.join(media_root, destination)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
        dst.write(src.read())
    
    return os.path.join(settings.MEDIA_URL, destination)


def _upload_s3(file_path: str, destination: str) -> Optional[str]:
    """Upload file to S3."""
    if not all([settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY, settings.AWS_STORAGE_BUCKET_NAME]):
        return None
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    
    try:
        s3_client.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, destination)
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{destination}"
    except Exception:
        return None
