from storages.backends.s3boto3 import S3Boto3Storage
from ecom.settings import *
class MinioMediaStorage(S3Boto3Storage):
    access_key = MINIO_ACCESS_KEY
    secret_key = MINIO_SECRET_KEY
    bucket_name = MINIO_BUCKET_NAME
    endpoint_url = f"http://{MINIO_ENDPOINT}:{MINIO_PORT}"
    use_ssl = False
    querystring_auth = False
    location = MINIO_LOCATION or ""
    region_name = "us-east-1"
    custom_domain = None 

    def url(self, name, parameters=None, expire=None):
        base = f"{MINIO_BASE_URL}/{self.bucket_name}"
        if self.location:
            base = f"{base}/{self.location}"
        return f"{base}/{name}"

