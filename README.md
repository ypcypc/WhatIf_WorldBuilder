# WhatIf_WorldBuilder

This project provides a pipeline to extract named entities from multilingual light novels. The entity pipeline performs candidate extraction, filtering, LLM classification, and alias clustering.

## Step 2 Example

Run the entity builder on chapters JSON and output `entities_final.json`:

```bash
poetry run python -m worldbuilder.pipelines.entity_pipeline chapters.json entities_final.json
```
