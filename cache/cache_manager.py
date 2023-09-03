import os

SAVE_PATH = "C:\LMTGIT\Python\AIDocuments\downloadedDocs"

def cache_content(content, post_id):
    txt_file_path = os.path.join(SAVE_PATH, f"{post_id}.txt")
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(content)

def get_cached_content(post_id):
    txt_file_path = os.path.join(SAVE_PATH, f"{post_id}.txt")
    if os.path.exists(txt_file_path):
        with open(txt_file_path, 'r') as txt_file:
            return txt_file.read()
    return None
