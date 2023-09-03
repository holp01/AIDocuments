# database_helper.py

import sqlite3  # Assuming SQLite, but you can use any database system.
import requests

DB_PATH = 'path_to_your_database.db'  # Replace with the path to your SQLite database.

def fetch_post_by_id(post_id):
    """
    Fetches a post from the database using its ID.
    :param post_id: ID of the post.
    :return: Dictionary representing the post, or None if not found.
    """
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM posts WHERE id=?", (post_id,))
    result = cursor.fetchone()
    
    connection.close()
    
    if not result:
        return None

    post = {
        'id': result[0],
        'title': result[1],
        'content': result[2],  # Assuming the 3rd column is the content.
        'pdf_url': result[3]   # Assuming the 4th column is the PDF URL.
    }
    return post

def download_pdf(pdf_url):
    """
    Downloads a PDF from a given URL.
    :param pdf_url: URL of the PDF.
    :return: Bytes of the downloaded PDF.
    """
    
    response = requests.get(pdf_url)
    response.raise_for_status()  # Raises exception when not a 2xx response.
    
    return response.content
