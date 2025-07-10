from worldbuilder.pipelines.alias_cluster import merge_entities
from worldbuilder.utils.schema import LlmEntity


def test_alias_cluster():
    e1 = LlmEntity(canonical="Veldora", aliases=[], type="Person")
    e2 = LlmEntity(canonical="ヴェルドラ", aliases=[], type="Person")
    merged = merge_entities([e1, e2])
    assert len(merged) == 1
