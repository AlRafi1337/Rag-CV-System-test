-- Removed markdown code block
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;


-- Documents table: one per source CV
CREATE TABLE IF NOT EXISTS documents (
id UUID PRIMARY KEY,
source_path TEXT NOT NULL,
original_filename TEXT NOT NULL,
mime_type TEXT,
sha256 CHAR(64) UNIQUE NOT NULL,
language TEXT,
created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
metadata JSONB DEFAULT '{}'::jsonb
);


-- Chunks table: semantic units for RAG
CREATE TABLE IF NOT EXISTS chunks (
id UUID PRIMARY KEY,
doc_id UUID REFERENCES documents(id) ON DELETE CASCADE,
chunk_index INT NOT NULL,
content TEXT NOT NULL,
tokens INT,
embedding vector(384),
tsv tsvector,
created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_chunks_tsv ON chunks USING GIN(tsv);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 200);


-- Simple candidates view
CREATE OR REPLACE VIEW v_doc_latest AS
SELECT d.*,
(SELECT count(*) FROM chunks c WHERE c.doc_id = d.id) as chunk_count
FROM documents d;