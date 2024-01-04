from pathlib import Path


def get_file_content(name: str) -> str:
    with Path(f"data/2023/{name}.txt").open(encoding="utf-8") as f:
        return f.read().rstrip("\n")
