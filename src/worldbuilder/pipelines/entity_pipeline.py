from __future__ import annotations
import json
from pathlib import Path
import asyncio
from .candidate_extractor import extract_candidates
from .candidate_filter import filter_top_k
from .llm_classifier import classify_all_batches
from .alias_cluster import merge_entities
from ..utils.schema import Chapter, LlmEntity


def build_entities(chapters_path: Path, out: Path):
    chapters_data = json.loads(chapters_path.read_text())
    chapters = [Chapter(**c) for c in chapters_data]
    candidates = extract_candidates(chapters)
    top = filter_top_k(candidates, k=800)
    llm_entities = asyncio.run(classify_all_batches(top))
    merged = merge_entities(llm_entities)
    out.write_text(json.dumps([e.dict() for e in merged], ensure_ascii=False, indent=2))
