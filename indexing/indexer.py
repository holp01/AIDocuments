import os
import pickle
import re
import pdb; 

# Location to save the index
INDEX_PATH = "C:\PythonAIFiles\index.pkl"

# Initialize an inverted index as a dictionary
# Example: {'word1': [post_id1, post_id3], 'word2': [post_id2, post_id3], ...}
inverted_index = {}

def tokenize(text):
    """
    Tokenizes a string into words. For simplicity, we'll split by non-alphanumeric characters.
    """
    return [word.lower() for word in re.findall(r'\w+', text)]

def update_index(content, post_id):
    """
    Tokenizes the content and updates the inverted index with the tokens.
    """
    global inverted_index

    tokens = tokenize(content)
    for token in tokens:
        if token not in inverted_index:
            inverted_index[token] = []
        if post_id not in inverted_index[token]:
            inverted_index[token].append(post_id)

    # Optionally, save the index to disk so it can be loaded later
    with open(INDEX_PATH, 'wb') as f:
        pickle.dump(inverted_index, f)

def search_index(query):
    """
    Searches the inverted index for posts related to the query.
    Returns a list of post_ids of matching posts.
    """
    tokens = tokenize(query)
    matching_posts = []

    for token in tokens:
        if token in inverted_index:
            matching_posts.extend(inverted_index[token])

    # Remove duplicates from the list
    matching_posts = list(set(matching_posts))

    return matching_posts
