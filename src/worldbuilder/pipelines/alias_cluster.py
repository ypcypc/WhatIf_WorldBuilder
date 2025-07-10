from __future__ import annotations
import re
from typing import List
from ..utils.schema import LlmEntity
from ..utils.sim import cosine_sim, pinyin_sim
from pypinyin import lazy_pinyin
from pykakasi import kakasi
import rapidfuzz

kks = kakasi()
kks.setMode("H", "a")
kks.setMode("K", "a")
kks.setMode("J", "a")
conv = kks.getConverter()

def romanize(text: str) -> str:
    jp = conv.do(text)
    if jp != text:
        return jp.lower()
    py = ''.join(lazy_pinyin(text))
    if py:
        return py.lower()
    return text.lower()

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

    def root_groups(self):
        roots = {}
        for idx in range(len(self.parent)):
            r = self.find(idx)
            roots.setdefault(r, []).append(idx)
        return roots.values()

def norm(text: str) -> str:
    text = re.sub(r"[·•．·,，.。!！?？:：\"'‘’“”《》〈〉]", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()

SIM_THR = 0.88
ROMAN_THR = 0.8
PINYIN_THR = 0.9

def merge_entities(llm_entities: List[LlmEntity]) -> List[LlmEntity]:
    if not llm_entities:
        return []
    groups = UnionFind(len(llm_entities))
    for i, a in enumerate(llm_entities):
        for j, b in enumerate(llm_entities[i+1:], i+1):
            if a.type != b.type:
                continue
            if norm(a.canonical) in norm(b.canonical) or norm(b.canonical) in norm(a.canonical):
                groups.union(i, j)
                continue
            sim = max(cosine_sim(a.canonical, b.canonical), pinyin_sim(a.canonical, b.canonical))
            if sim < SIM_THR:
                ra, rb = romanize(a.canonical), romanize(b.canonical)
                if rapidfuzz.distance.JaroWinkler.normalized_similarity(ra, rb) >= ROMAN_THR:
                    groups.union(i, j)
                    continue
            if sim >= SIM_THR:
                groups.union(i, j)
    merged: List[LlmEntity] = []
    for cluster in groups.root_groups():
        ents = [llm_entities[idx] for idx in cluster]
        aliases = {al for e in ents for al in ([e.canonical] + e.aliases)}
        canonical = max(ents, key=lambda e: len(e.aliases) + len(e.canonical)).canonical
        merged.append(LlmEntity(
            canonical=canonical,
            aliases=sorted(aliases - {canonical}),
            type=ents[0].type,
            protagonist=any(e.protagonist for e in ents)
        ))
    return merged
