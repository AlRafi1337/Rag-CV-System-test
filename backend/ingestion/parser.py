from typing import Tuple
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document as DocxDocument
import chardet


import os


SUPPORTED = {"application/pdf",
             "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain", "text/html"}


def detect_mime(filename: str) -> str:

    if filename.lower().endswith(".pdf"):
        return "application/pdf"
    if filename.lower().endswith(".docx"):
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if filename.lower().endswith(".html") or filename.lower().endswith(".htm"):
        return "text/html"
    return "text/plain"


def parse_file(path: str, mime: str | None = None) -> Tuple[str, dict]:

    mime = mime or detect_mime(path)
    text = ""
    meta = {}
    if mime == "application/pdf":
        text = pdf_extract(path)
    elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = DocxDocument(path)
        text = "\n".join(p.text for p in doc.paragraphs)
    elif mime == "text/html":
        with open(path, "rb") as f:
            raw = f.read()
        enc = chardet.detect(raw).get("encoding") or "utf-8"
        soup = BeautifulSoup(raw.decode(enc, errors="ignore"), "html.parser")
        text = soup.get_text(separator=" ")
    else:
        with open(path, "rb") as f:
            raw = f.read()
        enc = chardet.detect(raw).get("encoding") or "utf-8"
        text = raw.decode(enc, errors="ignore")
    return text, meta
