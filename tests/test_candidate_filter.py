from worldbuilder.pipelines.candidate_filter import is_candidate_ok
from worldbuilder.utils.schema import TokenInfo


def test_filter_noise():
    tok = TokenInfo(surface="对召唤主", first_chapter=1, count=5, sample=[])
    assert not is_candidate_ok(tok)
