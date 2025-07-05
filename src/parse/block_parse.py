import re

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []

    in_block: bool = False
    in_code_block: bool = False
    block_lines: list[str] = []
    for line in markdown.splitlines():
        if not in_code_block:
            line = line.strip()

        if line == "":
            if not in_block:
                continue
            else:
                in_block = False
                if in_code_block:
                    raise Exception("No closing ``` for code block")

                blocks.append("\n".join(block_lines))
                block_lines = []
        else:
            in_block = True
            if line.startswith("```"):
                in_code_block = not in_code_block
            block_lines.append(line)

    if len(block_lines) > 0:
        blocks.append("\n".join(block_lines))
    
    return blocks

def block_to_block_type(block: str) -> str:
    if re.match(r"^#{1,6} (.*)$", block):
        return "heading"

    if re.match(r"^```(.*)```$", block, re.DOTALL):
        return "code"

    block_lines = block.splitlines()

    quote_lines = re.findall(r"^>(?: (.*)|$)", block, re.MULTILINE)
    if len(quote_lines) == len(block_lines):
        return "quote"

    ul_dash_lines = re.findall(r"^[-](?: (.*)|)$", block, re.MULTILINE)
    if len(ul_dash_lines) == len(block_lines):
        return "unordered_list"

    ul_asterisk_lines = re.findall(r"^[*](?: (.*)|)$", block, re.MULTILINE)
    if len(ul_asterisk_lines) == len(block_lines):
        return "unordered_list"

    is_ordered_list = True
    for line_num, line in enumerate(block_lines):
        if not re.match(rf"^{line_num + 1}\. (.*)$", line):
            is_ordered_list = False
            break
    if is_ordered_list:
        return "ordered_list"

    return "paragraph"

def extract_title(markdown: str) -> str:
    heading_match = re.search(r"^# (.*)$", markdown, re.MULTILINE)
    if heading_match is None:
        raise Exception("Couldn't find a level 1 heading in markdown")
    
    return heading_match.group(1)