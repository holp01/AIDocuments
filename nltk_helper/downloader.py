import os
import nltk
import zipfile
from azure.storage.blob import BlobServiceClient

def download_nltk_data():
    NLTK_DATA_DIR = '/tmp/nltk_data'  # Temporary directory in Linux

    # Check if NLTK data is present
    if not os.path.exists(NLTK_DATA_DIR):
        os.mkdir(NLTK_DATA_DIR)
        # Assuming you've set up Azure Blob Storage details as environment variables or elsewhere
        AZURE_BLOB_CONNECTION_STRING = os.environ.get('AZURE_BLOB_CONNECTION_STRING')
        BLOB_CONTAINER_NAME = os.environ.get('BLOB_CONTAINER_NAME')
        
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=BLOB_CONTAINER_NAME, blob='stopwords.zip')
        zip_path = f"{NLTK_DATA_DIR}/stopwords.zip"
        with open(zip_path, 'wb') as download_file:
            data = blob_client.download_blob()
            data.readinto(download_file)

        # Unzip the file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(NLTK_DATA_DIR)

    # Point NLTK to the right directory
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
