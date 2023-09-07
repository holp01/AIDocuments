import os
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter
from whoosh import qparser
import re

# Define the schema for the index
schema = Schema(id =TEXT(stored=True),title=TEXT(stored=True), content=TEXT(stored=True))

# Directory to save the Whoosh index
INDEX_DIR  = "C:\PythonAIFiles\index.pkl"

def create_or_open_index(index_dir=INDEX_DIR):
    """Create a new index or open an existing one."""
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        return create_in(index_dir, schema)
    else:
        return open_dir(index_dir)

def update_index(title, content, mdFile):
    """Add new content to the index or update existing content."""
    index = create_or_open_index()
    writer = AsyncWriter(index)
    writer.update_document(id= mdFile, title=title, content=content)
    writer.commit()
    
def search_index(query):
    """Search the index based on a query and return matching topics."""
    index = create_or_open_index()
    with index.searcher() as searcher:
        sanitized_query = re.sub(r'[?]', '', query)  # Remove special characters like '?'
        
        query_parser = QueryParser("content", index.schema, group=qparser.OrGroup)
        parsed_query = query_parser.parse(sanitized_query)
        
        print("Sanitized Query:", sanitized_query)
        print("Parsed Query:", parsed_query)
        
        results = searcher.search(parsed_query, limit=None)  # Set limit=None to retrieve all matching results
        print("Number of Hits:", len(results))
        
        return [hit["id"] for hit in results]

