from apps.utils.minio import minio_s3
        
def handle_upload(files, folder: str = "") -> str | None:
    uploaded_files = []

    for f in files:
        if folder:
            upload_path = minio_s3.minio_upload_file(f, f.name, folder)
        else:
            upload_path = minio_s3.minio_upload_file(f, f.name)
        if upload_path is None:
            return None
        uploaded_files.append(upload_path)

    return ";".join(uploaded_files)
