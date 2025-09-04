import uuid
from sqlalchemy import Column, String, Text, Integer, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Document(Base):

    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_path = Column(Text, nullable=False)
    original_filename = Column(Text, nullable=False)
    mime_type = Column(String, nullable=True)
    sha256 = Column(String(64), unique=True, nullable=False)
    language = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), onupdate=func.now())
    metadata = Column(JSON, default=dict)
    chunks = relationship("Chunk", back_populates="document",
                          cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey(
        "documents.id", ondelete="CASCADE"))
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer, nullable=True)
    # stored via direct SQL insert to vector
    embedding = Column("embedding", Text, nullable=True)
    tsv = Column("tsv", Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    document = relationship("Document", back_populates="chunks")
