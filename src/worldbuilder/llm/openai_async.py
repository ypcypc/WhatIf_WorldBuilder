from __future__ import annotations
import json
import asyncio
from pathlib import Path
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
import aiofiles
from ..utils.schema import TokenInfo, LlmEntity
import openai

client = openai.AsyncOpenAI()
CACHE_DIR = Path("cache/llm")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SYSTEM = "You are a multilingual light-novel entity curator"
function_schema = {
    "name": "add_entities",
    "parameters": {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "canonical": {"type": "string"},
                        "aliases": {"type": "array", "items": {"type": "string"}},
                        "type": {"enum": ["Person", "Place", "Item", "Other"]},
                        "protagonist": {"type": "boolean"},
                    },
                    "required": ["canonical", "type"],
                },
            }
        },
        "required": ["entities"],
    },
}

async def _call_openai(payload: str) -> str:
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM},
                 {"role": "user", "content": f"```json\n{payload}\n```"}],
        tools=[{"type": "function", "function": function_schema}],
        tool_choice={"type": "function", "function": {"name": "add_entities"}},
        temperature=0
    )
    return resp.choices[0].message.tool_calls[0].function.arguments

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2))
async def classify_batch(batch: List[TokenInfo]) -> List[LlmEntity]:
    payload = json.dumps([t.dict() for t in batch], ensure_ascii=False)
    key = str(hash(payload))
    cache_path = CACHE_DIR / f"{key}.json"
    if cache_path.exists():
        async with aiofiles.open(cache_path, 'r') as f:
            data = json.loads(await f.read())
    else:
        args = await _call_openai(payload)
        data = json.loads(args)
        async with aiofiles.open(cache_path, 'w') as f:
            await f.write(json.dumps(data, ensure_ascii=False))
    return [LlmEntity(**e) for e in data["entities"]]
