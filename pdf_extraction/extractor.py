# extractor.py

import PyPDF2
from io import BytesIO
import re

def extract_from_pdf(pdf_content):
    """
    Extracts text content from a given PDF.
    :param pdf_content: Bytes representing the PDF content.
    :return: Extracted text from the PDF.
    """
    
    with BytesIO(pdf_content) as pdf_file:
        reader = PyPDF2.PdfFileReader(pdf_file)
        text = ''
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text += page.extractText()
            
    return text

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
    return preprocess_md(content)

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

