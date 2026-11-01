"""S3-compatible storage for Cloudflare R2 (staging/prod) and MinIO (local).

Private files (submissions, lecture video, packages) are only ever served through
short-lived signed URLs. Public files (catalog images, certificate PDFs that are
meant to be shared) live in a separate bucket.
"""

from storages.backends.s3 import S3Storage


class PrivateStorage(S3Storage):
    default_acl = None
    querystring_auth = True
    querystring_expire = 15 * 60  # seconds
    file_overwrite = False


class PublicStorage(S3Storage):
    default_acl = None
    querystring_auth = False
    file_overwrite = False
