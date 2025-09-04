from sqlalchemy import text
from database import SessionLocal
from embeddings.factory import get_provider
from config import settings
from loguru import logger


provider = get_provider()


SQL_HYBRID = text("""
WITH q AS (
SELECT :q::text AS qtxt
), qemb AS (
SELECT (:emb)::vector AS v
)
SELECT c.id as chunk_id, c.doc_id, d.original_filename,
(1 - (c.embedding <=> (SELECT v FROM qemb))) AS sem_score,
ts_rank(c.tsv, to_tsvector('simple', unaccent((SELECT qtxt FROM q)))) AS kw_score,
(0.7 * (1 - (c.embedding <=> (SELECT v FROM qemb))) + 0.3 * ts_rank(c.tsv, to_tsvector('simple', unaccent((SELECT qtxt FROM q))))) AS score,
c.content
FROM chunks c
JOIN documents d ON d.id = c.doc_id
ORDER BY score DESC
LIMIT :k
""")


SQL_DOCS = text("SELECT id, original_filename, mime_type, created_at, metadata, (SELECT COUNT(*) FROM chunks cc WHERE cc.doc_id = d.id) as chunk_count FROM documents d ORDER BY created_at DESC LIMIT :n")


def search(query: str, k: int = 20):

    vec = provider.embed([query])[0]
    emb = f"[{', '.join(map(lambda x: f'{x:.6f}', vec))}]"
    with SessionLocal() as db:
        rows = db.execute(
            SQL_HYBRID, {"q": query, "emb": emb, "k": k}).mappings().all()
    return [dict(r) for r in rows]


def list_documents(n: int = 100):

    with SessionLocal() as db:
        rows = db.execute(SQL_DOCS, {"n": n}).mappings().all()
    return [dict(r) for r in rows]
