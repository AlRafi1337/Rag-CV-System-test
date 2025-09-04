import time

import time
import os
import tempfile
import uuid
from email import message_from_bytes
from database import SessionLocal
from config import settings
from loguru import logger
from nlp.chunking import sliding_window_chunks
from embeddings.factory import get_provider
provider = get_provider()

SQL_INSERT_DOC = "..."  # TODO: fill in actual SQL
SQL_INSERT_CHUNK = "..."  # TODO: fill in actual SQL


def process_attachment(db, filepath, filename, mime=None, file_hash=None, meta=None, text_content=None):
    doc_id = uuid.uuid4()
    res = db.execute(SQL_INSERT_DOC, {
        'id': doc_id,
        'source_path': filepath,
        'original_filename': filename,
        'mime_type': mime,
        'sha256': file_hash,
        'metadata': meta or {"source": "email"},
    }).fetchone()
    if not res:
        logger.info(f"Duplicate email attachment skipped: {filename}")
        return
    doc_id = res[0]
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
    logger.info(
        f"Email attachment saved: {filename} -> {doc_id} chunks={len(chunks)}")


def run_imap_poll():

    if not settings.imap_host or not settings.imap_username or not settings.imap_password:
        logger.error("IMAP settings missing; skipping email ingestion")
        return
    from imapclient import IMAPClient
    with IMAPClient(settings.imap_host, port=settings.imap_port, ssl=True) as server:
        server.login(settings.imap_username, settings.imap_password)
        server.select_folder(settings.imap_folder)
        seen = set()
        logger.info("Started IMAP poller")
        while True:
            # could switch to IDLE in the future
            messages = server.search(["UNSEEN"])
            with SessionLocal() as db:
                for uid in messages:
                    if uid in seen:
                        continue
                    seen.add(uid)
                    raw = server.fetch(uid, [b'RFC822'])[uid][b'RFC822']
                    msg = message_from_bytes(raw)
                    for part in msg.walk():
                        if part.get_content_disposition() == 'attachment':
                            filename = part.get_filename() or "attachment"
                            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                                tmp.write(part.get_payload(decode=True))
                                tmp_path = tmp.name
                            try:
                                process_attachment(db, tmp_path, filename)
                            finally:
                                try:
                                    os.remove(tmp_path)
                                except Exception:
                                    pass
            time.sleep(settings.imap_poll_seconds)


if __name__ == '__main__':
    run_imap_poll()
