from __future__ import annotations
import re
import numpy as np
from ..utils.schema import TokenInfo

STOP_PREFIX = {"对", "这", "该", "その", "この", "the", "a", "an"}
STOP_SUFFIX = {"东西", "问题", "事情"}
MIN_LEN, MAX_LEN = 2, 30


def is_candidate_ok(tok: TokenInfo) -> bool:
    t = tok.surface.strip(" ·•·,，.。!！?？:：\"'《》“”")
    if not (MIN_LEN <= len(t) <= MAX_LEN):
        return False
    if t[0] in STOP_PREFIX or t[-2:] in STOP_SUFFIX:
        return False
    if re.fullmatch(r'[^\w\u4e00-\u9fff]+', t):
        return False
    return True


def filter_top_k(tokens: list[TokenInfo], k: int = 800) -> list[TokenInfo]:
    tokens = [t for t in tokens if is_candidate_ok(t)]
    tf = np.array([t.count for t in tokens], dtype=float)
    if len(tf) == 0:
        return []
    tfidf_z = (tf - tf.mean()) / tf.std()
    filtered = [t for t, z in zip(tokens, tfidf_z) if z > 0]
    return sorted(filtered, key=lambda t: t.count, reverse=True)[:k]
