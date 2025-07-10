import re

SENTENCE_END = re.compile(r'[.!?。！？]')

def get_sentence_with_token(text: str, token: str) -> str:
    idx = text.find(token)
    if idx == -1:
        return text[:120]
    start = text.rfind('\n', 0, idx)
    start = 0 if start == -1 else start
    end = SENTENCE_END.search(text, idx)
    end_idx = end.end() if end else len(text)
    return text[start:end_idx].strip()
