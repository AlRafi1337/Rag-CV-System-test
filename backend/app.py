

from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy import text
import uuid
from database import get_db
from config import settings
from search.service import list_documents, search as svc_search
from search.graph import build_graph
from ingestion.parser import parse_file, detect_mime
from ingestion.dedupe import sha256_file
from nlp.chunking import sliding_window_chunks
from embeddings.factory import get_provider
from database import get_db
from config import settings


provider = get_provider()

app = FastAPI()


@app.get("/documents")
async def documents():
    return list_documents()


@app.post("/search")
async def search(payload: dict):
    q = payload.get("query", "")
    k = int(payload.get("k", 20))
    results = svc_search(q, k)
    return {"results": results}


@app.post("/search/graph")
async def search_graph(payload: dict):
    q = payload.get("query", "")
    k = int(payload.get("k", 20))
    results = svc_search(q, k)
    return build_graph(q, results)


@app.post("/upload")
async def upload(files: list[UploadFile] = File(...), db=Depends(get_db)):
    out = []
    for uf in files:
        path = f"/tmp/{uf.filename}"
        content = await uf.read()
        with open(path, "wb") as f:
            f.write(content)
        mime = detect_mime(path)
        text_content, meta = parse_file(path, mime)
        if not text_content:
            continue
        file_hash = sha256_file(path)
        doc_id = uuid.uuid4()
        res = db.execute(text("""
            INSERT INTO documents (id, source_path, original_filename, mime_type, sha256, metadata)
            VALUES (:id, :source_path, :original_filename, :mime_type, :sha256, :metadata)
            ON CONFLICT (sha256) DO NOTHING RETURNING id
        """), {
            'id': doc_id,
            'source_path': path,
            'original_filename': uf.filename,
            'mime_type': mime,
            'sha256': file_hash,
            'metadata': meta or {},
        }).fetchone()
        if not res:
            continue
        doc_id = res[0]
        chunks = sliding_window_chunks(
            text_content, settings.chunk_size, settings.chunk_overlap)
        vectors = provider.embed(chunks)
        for idx, (chunk_text, vec) in enumerate(zip(chunks, vectors)):
            db.execute(text("""
                INSERT INTO chunks (id, doc_id, chunk_index, content, tokens, embedding, tsv)
                VALUES (:id, :doc_id, :chunk_index, :content, :tokens, :embedding::vector, to_tsvector('simple', unaccent(:content)))
            """), {
                'id': uuid.uuid4(),
                'doc_id': doc_id,
                'chunk_index': idx,
                'content': chunk_text,
                'tokens': len(chunk_text.split()),
                'embedding': f"[{', '.join(map(lambda x: f'{x:.6f}', vec))}]",
            })
        db.commit()
        out.append(
            {"doc_id": str(doc_id), "filename": uf.filename, "chunks": len(chunks)})
    return {"ingested": out}
