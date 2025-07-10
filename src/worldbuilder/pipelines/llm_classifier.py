from __future__ import annotations
import asyncio
from typing import List
import more_itertools
from ..utils.schema import TokenInfo, LlmEntity
from ..llm.openai_async import classify_batch

BATCH_SIZE = 50

async def classify_all_batches(candidates: List[TokenInfo]) -> List[LlmEntity]:
    batches = more_itertools.chunked(candidates, BATCH_SIZE)
    results = await asyncio.gather(*(classify_batch(list(b)) for b in batches))
    llm_entities = [e for batch in results for e in batch]
    return llm_entities
