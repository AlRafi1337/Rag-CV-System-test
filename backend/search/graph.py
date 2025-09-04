from collections import defaultdict
from typing import Dict, Any, List


# Build a simple graph: query node connected to chunks; chunks to doc nodes


def build_graph(query: str, results: List[dict]) -> dict:
    nodes = []
    edges = []

    nodes.append({"id": "query", "label": query, "type": "query"})

    doc_nodes = {}
    chunk_nodes = {}

    for r in results:
        did = str(r["doc_id"])  # document id
        cid = str(r["chunk_id"])  # chunk id
        if did not in doc_nodes:
            doc_nodes[did] = {
                "id": did, "label": r["original_filename"], "type": "document"}
        if cid not in chunk_nodes:
            chunk_nodes[cid] = {"id": cid, "label": r["content"][:120] +
                                ("…" if len(r["content"]) > 120 else ""), "type": "chunk", "score": r["score"]}
        edges.append({"source": "query", "target": cid, "weight": r["score"]})
        edges.append({"source": cid, "target": did, "weight": r["score"]})

    nodes.extend(doc_nodes.values())
    nodes.extend(chunk_nodes.values())
    return {"nodes": nodes, "edges": edges}
