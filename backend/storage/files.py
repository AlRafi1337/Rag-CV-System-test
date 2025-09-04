import os
from config import settings


ROOT = settings.file_storage_root


def ensure_storage_root():
    os.makedirs(ROOT, exist_ok=True)


def save_uploaded_file(fileobj, filename: str) -> str:
    ensure_storage_root()
    out = os.path.join(ROOT, filename)
    base, ext = os.path.splitext(out)
    i = 1
    while os.path.exists(out):
        out = f"{base}_{i}{ext}"
        i += 1
    with open(out, 'wb') as f:
        for chunk in iter(lambda: fileobj.read(8192), b''):
            f.write(chunk)
    return out
