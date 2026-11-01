"""Create the S3 buckets if they are missing. Used for local MinIO and staging."""

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the public and private storage buckets if they do not exist."

    def handle(self, *args: object, **options: object) -> None:
        client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name="us-east-1",
        )
        for bucket in (settings.S3_BUCKET_PRIVATE, settings.S3_BUCKET_PUBLIC):
            try:
                client.head_bucket(Bucket=bucket)
                self.stdout.write(f"Bucket {bucket} exists.")
            except ClientError:
                client.create_bucket(Bucket=bucket)
                self.stdout.write(self.style.SUCCESS(f"Created bucket {bucket}."))
