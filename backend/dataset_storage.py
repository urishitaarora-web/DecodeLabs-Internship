import os
from supabase import create_client


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv(
    "SUPABASE_SERVICE_ROLE_KEY"
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)


BUCKET_NAME = "datasets"


def upload_dataset(
    storage_path: str,
    file_bytes: bytes,
    content_type: str | None = None,
):
    options = {}

    if content_type:
        options["content-type"] = content_type

    return supabase.storage.from_(
        BUCKET_NAME
    ).upload(
        storage_path,
        file_bytes,
        options=options,
    )


def download_dataset(storage_path: str):
    return (
        supabase.storage
        .from_(BUCKET_NAME)
        .download(storage_path)
    )


def delete_dataset(storage_path: str):
    return (
        supabase.storage
        .from_(BUCKET_NAME)
        .remove([storage_path])
    )