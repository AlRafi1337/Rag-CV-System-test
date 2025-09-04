from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class DocumentOut(BaseModel):
    id: UUID
    original_filename: str
    mime_type: Optional[str]
    created_at: str
    metadata: dict
    chunk_count: Optional[int] = None


class SearchRequest(BaseModel):
    query: str
    k: int = 20
    filters: Optional[dict] = None


class ScoredChunk(BaseModel):
    doc_id: UUID
    chunk_id: UUID
    score: float
    content: str
    filename: str


class GraphResponse(BaseModel):
    nodes: list
    edges: list
