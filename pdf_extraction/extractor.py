# extractor.py

import re

def extract_from_txt(file_path):
    """Extract content from a txt file."""
    with open(file_path, 'r') as file:
        return file.read()

def read_md_file(file_path):
    """Read content from a .md file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def extract_from_md(file_path):
    """Extract and preprocess content from a .md file."""
    content = read_md_file(file_path)
    title, content = split_title_and_content(content)
    content = preprocess_md(content)
    return title, content

def extract_from_md_content(content):
    """Extract and preprocess content directly from a .md content string."""
    content = split_title_and_content(content)
    content = preprocess_md(content)
    return content

def split_title_and_content(content):
    lines = content.split("\n")
    content = "\n".join(lines[0:])
    return content

def preprocess_md(content):
    # Remove headers (e.g., #, ##, ###, etc.)
    content = re.sub(r'^#+\s?', '', content, flags=re.MULTILINE)

    # Remove inline links (e.g., [text](URL))
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # Remove bold, italics, etc.
    content = re.sub(r'[_*]{1,2}([^_*]+)[_*]{1,2}', r'\1', content)

    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove inline code (e.g., `code`)
    content = re.sub(r'`([^`]+)`', r'\1', content)

    # Remove images (e.g., ![alt text](URL))
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # Further processing can be added as needed
    return content.strip()

