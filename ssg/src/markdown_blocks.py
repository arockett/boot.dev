
def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [b.strip() for b in markdown.split("\n\n")]
    return [b for b in blocks if len(b) > 0]
