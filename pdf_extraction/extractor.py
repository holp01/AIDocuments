# extractor.py

import PyPDF2
from io import BytesIO

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
