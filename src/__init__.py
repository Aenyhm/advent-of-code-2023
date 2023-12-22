def get_file_content(name: str) -> str:
    return open(f"data/2023/{name}.txt", encoding="utf-8").read().rstrip('\n')
