from io import BytesIO

from minio import Minio
from PIL import Image

from ecom.settings import *

minio_client = Minio(
    endpoint=f"{MINIO_ENDPOINT}:{MINIO_PORT}",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def connect_minio_client(endpoint, port, access_key, secret_key, secure = False):
    return Minio(
        endpoint=f"{endpoint}:{port}",
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )
   

# Upload file lên MinIO
def upload_minio(minio_client, base_url, bucket_name, object_name, data, content_type):
    try:
        result = minio_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            length=len(data.getvalue()),
            content_type=content_type
        )
        return f"{base_url}/{bucket_name}/{object_name}", None
    except Exception as e:
        print("Error upload_minio:", e)
        return None, "Lỗi khi upload Minio"


def upload_image(file, filename, format="JPEG"):
    if not filename.lower().endswith(f".{format.lower()}"):
        filename = f"{filename}.{format.lower()}"

    object_name = f"{MINIO_LOCATION}/{filename}"

    if hasattr(file, "read"):
        file.seek(0)
        image = Image.open(file)
    else:
        raise ValueError("File không hợp lệ")

    img_bytes = BytesIO()

    if format.upper() == "JPEG":
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        else:
            image = image.convert("RGB")
    elif format.upper() == "PNG":
        image = image.convert("RGBA")

    image.save(img_bytes, format=format)
    img_bytes.seek(0)

    length = img_bytes.getbuffer().nbytes
    content_type = f"image/{format.lower()}"
    minio_client.put_object(
        bucket_name=MINIO_BUCKET_NAME,
        object_name=object_name,
        data=img_bytes,
        length=length,
        content_type=content_type
    )

    file_url = f"{MINIO_BASE_URL}/{MINIO_BUCKET_NAME}/{object_name}"
    return file_url
