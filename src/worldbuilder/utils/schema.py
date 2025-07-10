from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

class Chapter(BaseModel):
    id: int
    raw_text: str

class TokenInfo(BaseModel):
    surface: str
    first_chapter: int
    count: int
    sample: List[str]

class LlmEntity(BaseModel):
    canonical: str
    aliases: List[str] = []
    type: str
    protagonist: bool = False
