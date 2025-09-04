from typing import Iterable


def sliding_window_chunks(text: str, chunk_size: int, overlap: int) -> Iterable[str]:

    words = text.split()
    if not words:
        return []
    step = max(1, chunk_size - overlap)
    out = []
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk:
            out.append(chunk)
    return out
