from pathlib import Path
from .entity_pipeline import build_entities
import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m worldbuilder.pipelines <chapters.json> <out.json>")
        sys.exit(1)
    build_entities(Path(sys.argv[1]), Path(sys.argv[2]))
