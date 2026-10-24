
import boto3
import os

S3_ENDPOINT_URL = os.getenv(
    "S3_ENDPOINT_URL",
    "http://localhost:4566"
)

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
    "event-announcement-assets-demo-2026"
)

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)

def upload_banner(file_obj, filename, content_type):
    s3_client.upload_fileobj(
        file_obj,
        S3_BUCKET_NAME,
        filename,
        ExtraArgs={"ContentType": content_type},
    )

    return f"s3://{S3_BUCKET_NAME}/{filename}"


def get_banner(filename):
    response = s3_client.get_object(
        Bucket=S3_BUCKET_NAME,
        Key=filename,
    )
    return response["Body"].read(), response.get("ContentType", "application/octet-stream")

