import base64
import mimetypes
from io import BytesIO
from minio import Minio
from ecom.settings import (
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_ENDPOINT,
    MINIO_PORT,
    MINIO_BUCKET_NAME,
    MINIO_LOCATION,
    MINIO_BASE_URL,
)


class S3Minio:
    @staticmethod
    def get_minio_client():
        return Minio(
            endpoint=f"{MINIO_ENDPOINT}:{MINIO_PORT}",
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )

    @staticmethod
    def minio_upload_file(file, file_name: str, folder: str = "") -> str | None:
        try:
            client = S3Minio.get_minio_client()
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
                object_name = f"{MINIO_LOCATION}/{folder}/{file_name}"
            else:
                object_name = f"{MINIO_LOCATION}/{file_name}"

            client.put_object(
                bucket_name=MINIO_BUCKET_NAME,
                object_name=object_name,
                data=data,
                length=lenfile,
                content_type=content_type,
            )

            return f"{MINIO_BASE_URL}/{MINIO_BUCKET_NAME}/{object_name}"

        except Exception as e:
            print(f"Upload error: {e}")
            return None

    @staticmethod
    def ping() -> bool:
        try:
            client = S3Minio.get_minio_client()
            client.bucket_exists(MINIO_BUCKET_NAME)
            return True
        except Exception:
            return False