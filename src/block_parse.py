def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []

    in_block: bool = False
    block_lines: list[str] = []
    for line in markdown.splitlines():
        line = line.strip()
        if line == "":
            if not in_block:
                continue
            else:
                in_block = False
                blocks.append("\n".join(block_lines))
                block_lines = []
        else:
            in_block = True
            block_lines.append(line)

    if len(block_lines) > 0:
        blocks.append("\n".join(block_lines))
    
    return blocks

