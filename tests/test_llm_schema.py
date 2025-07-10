from worldbuilder.utils.schema import LlmEntity


def test_llm_schema():
    ent = LlmEntity(canonical="Test", aliases=["T"], type="Person")
    assert ent.canonical == "Test"
