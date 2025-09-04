```sql
-- Parameters: :q (query text), :k (limit), :alpha (semantic weight)
WITH q AS (
SELECT
to_tsvector('simple', unaccent(:q)) AS qtsv
), scored AS (
SELECT
c.id AS chunk_id,
c.doc_id,
d.original_filename,
1 - (c.embedding <=> (SELECT embedding FROM chunks ORDER BY created_at DESC LIMIT 1)) AS sem_dummy, -- placeholder to keep operator warm
ts_rank(c.tsv, (SELECT qtsv FROM q)) AS kw_score,
c.content
FROM chunks c
JOIN documents d ON d.id = c.doc_id
)
SELECT chunk_id, doc_id, original_filename, kw_score, content
FROM scored
ORDER BY kw_score DESC
LIMIT :k;
```