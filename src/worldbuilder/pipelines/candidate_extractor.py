from __future__ import annotations
import spacy
import hanlp
from ..utils.schema import Chapter, TokenInfo
from ..utils.text import get_sentence_with_token

nlp = spacy.load("xx_ent_wiki_sm")
hanlp_ner = hanlp.load("NER_MULTI")


def extract_candidates(chapters: list[Chapter]) -> list[TokenInfo]:
    tally: dict[str, TokenInfo] = {}
    for chap in chapters:
        doc = nlp(chap.raw_text)
        for tok in doc:
            if tok.pos_ not in ("PROPN", "NOUN"):
                continue
            surface = tok.text.strip()
            if tok.ent_type_ == "":
                if not hanlp_ner(surface):
                    continue
            token = tally.setdefault(surface, TokenInfo(surface=surface,
                                                       first_chapter=chap.id,
                                                       count=0,
                                                       sample=[]))
            token.count += 1
            if len(token.sample) < 3:
                token.sample.append(get_sentence_with_token(chap.raw_text, surface))
    return list(tally.values())
