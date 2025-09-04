
import os
import uuid
import time
from database import SessionLocal
from config import settings
from loguru import logger
from nlp.chunking import sliding_window_chunks
from embeddings.factory import get_provider
provider = get_provider()

SQL_INSERT_DOC = "..."  # TODO: fill in actual SQL
SQL_INSERT_CHUNK = "..."  # TODO: fill in actual SQL


def ingest_one(db, filepath, filename=None, mime=None, file_hash=None, meta=None, text_content=None):
    res = db.execute(SQL_INSERT_DOC, {
        'id': uuid.uuid4(),
        'source_path': filepath,
        'original_filename': filename or os.path.basename(filepath),
        'mime_type': mime,
        'sha256': file_hash,
        'metadata': meta or {},
    }).fetchone()
    if not res:
        logger.info(f"Duplicate (by sha256), skipped: {filepath}")
        return
    doc_id = res[0]
    # chunk
    chunks = sliding_window_chunks(
        text_content, settings.chunk_size, settings.chunk_overlap)
    vectors = provider.embed(chunks)
    for idx, (chunk_text, vec) in enumerate(zip(chunks, vectors)):
        db.execute(SQL_INSERT_CHUNK, {
            'id': uuid.uuid4(),
            'doc_id': doc_id,
            'chunk_index': idx,
            'content': chunk_text,
            'tokens': len(chunk_text.split()),
            'embedding': f"[{', '.join(map(lambda x: f'{x:.6f}', vec))}]",
        })
    db.commit()
    logger.info(f"Ingested {filepath} as {doc_id}; chunks={len(chunks)}")


def expand_paths(p: str) -> list:
    if os.path.isdir(p):
        out = []
        for root, _, files in os.walk(p):
            for fn in files:
                out.append(os.path.join(root, fn))
        return out
    return [p]


def main(paths, watch=False, interval=10):
    with SessionLocal() as db:
        while True:
            for p in paths:
                for f in expand_paths(p):
                    ingest_one(db, f)
            if not watch:
                break
            time.sleep(interval)


if __name__ == '__main__':
    # Example usage: main(["/path/to/data"], watch=False)
    main(["/path/to/data"], watch=False)
