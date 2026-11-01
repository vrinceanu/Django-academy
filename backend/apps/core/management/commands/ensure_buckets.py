"""Check that the S3 (R2) buckets exist, creating them if the key is allowed to.

Does nothing when files are stored on local disk (no S3_ENDPOINT_URL).
"""

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the public and private storage buckets if they do not exist."

    def handle(self, *args: object, **options: object) -> None:
        if not settings.USE_S3:
            self.stdout.write("Files are stored on local disk; no buckets to check.")
            return
        client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name="auto",
        )
        for bucket in (settings.S3_BUCKET_PRIVATE, settings.S3_BUCKET_PUBLIC):
            try:
                client.head_bucket(Bucket=bucket)
                self.stdout.write(f"Bucket {bucket} exists.")
            except ClientError:
                try:
                    client.create_bucket(Bucket=bucket)
                except ClientError as exc:
                    raise CommandError(
                        f"Bucket {bucket} is missing and this key cannot create it. "
                        "Create it in the Cloudflare dashboard (R2)."
                    ) from exc
                self.stdout.write(self.style.SUCCESS(f"Created bucket {bucket}."))
