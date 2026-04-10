import base64
import mimetypes
from io import BytesIO
import time
from minio import Minio
from apps.logging import logging_log as lg
from django.conf import settings


class S3Minio:
    _instance = None
    _initialized = False
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not self._initialized:
            self.MINIO_ENDPOINT = settings.MINIO_ENDPOINT
            self.MINIO_PORT = settings.MINIO_PORT
            self.MINIO_ACCESS_KEY = settings.MINIO_ACCESS_KEY
            self.MINIO_SECRET_KEY = settings.MINIO_SECRET_KEY
            self.MINIO_BUCKET_NAME = settings.MINIO_BUCKET_NAME
            self.MINIO_LOCATION = settings.MINIO_LOCATION
            self.MINIO_BASE_URL = settings.MINIO_BASE_URL
            self._initialized = True
    def get_minio_client(self):
        return Minio(
            endpoint=f"{self.MINIO_ENDPOINT}:{self.MINIO_PORT}",
            access_key=self.MINIO_ACCESS_KEY,
            secret_key=self.MINIO_SECRET_KEY,
            secure=False,
        )
    def minio_upload_file(self, file, file_name: str, folder: str = "") -> str | None:
        try:
            client = self.get_minio_client()
            if isinstance(file, str):
                if file.startswith("data:"):
                    file = file.split(",", 1)[1]
                file = base64.b64decode(file)
            elif hasattr(file, "read"):
                file = file.read()

            content_type, _ = mimetypes.guess_type(file_name)
            if not content_type:
                content_type = "application/octet-stream"

            data = BytesIO(file)
            lenfile = len(file)

            if folder:
                object_name = f"{self.MINIO_LOCATION}/{folder}/{file_name}"
            else:
                object_name = f"{self.MINIO_LOCATION}/{file_name}"

            client.put_object(
                bucket_name=self.MINIO_BUCKET_NAME,
                object_name=object_name,
                data=data,
                length=lenfile,
                content_type=content_type,
            )
            lg.log_info(
                message=f"[Upload] Success",
                file_name=file_name,
                object_name=object_name
            )

            return f"{self.MINIO_BASE_URL}/{self.MINIO_BUCKET_NAME}/{object_name}"

        except Exception:
            lg.log_error(
                message=f"[Upload] Error"
            )
            return None
        
    def ping(self):
        start = time.perf_counter()
        try:
            client = self.get_minio_client()
            client.bucket_exists(self.MINIO_BUCKET_NAME)
            return "WARNING" if (time.process_time() - start > 3) else "NORMAL"
        except Exception:
            lg.log_error(message=f"[Minio][PING] Error")
            return "CRITICAL"