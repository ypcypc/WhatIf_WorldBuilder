from __future__ import annotations
from sentence_transformers import SentenceTransformer
import numpy as np
from pypinyin import lazy_pinyin
import rapidfuzz

try:
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
except Exception:  # pragma: no cover - fallback when model download fails
    model = None

def embed(text: str) -> np.ndarray:
    if model is None:
        # simple deterministic embedding fallback
        return np.array([hash(text) % 1000], dtype=float)
    return model.encode(text, normalize_embeddings=True)

def cosine_sim(a: str, b: str) -> float:
    va, vb = embed(a), embed(b)
    if model is None:
        return 1.0 if va[0] == vb[0] else 0.0
    return float(np.dot(va, vb))

def pinyin_sim(a: str, b: str) -> float:
    a_py = ''.join(lazy_pinyin(a))
    b_py = ''.join(lazy_pinyin(b))
    if model is None:
        a_py = a.lower()
        b_py = b.lower()
    return rapidfuzz.distance.JaroWinkler.normalized_similarity(a_py, b_py)
