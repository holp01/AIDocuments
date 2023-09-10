import os
import nltk
import zipfile
from azure.storage.blob import BlobServiceClient
from azurehelper import azure_manager

def download_nltk_data():
    NLTK_DATA_DIR = '/home/data/nltk_data'  # Updated path

    print("Checking if NLTK data directory exists...")
    # Check if NLTK data is present
    if not os.path.exists(NLTK_DATA_DIR):
        print("Creating NLTK data directory...")
        os.makedirs(NLTK_DATA_DIR, exist_ok=True)  # Using makedirs to create any necessary parent directories
        
        # Assuming you've set up Azure Blob Storage details as environment variables or elsewhere
        BLOB_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        CONTAINER_NAME = os.environ.get('BLOB_CONTAINER_NAME')
        
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob='stopwords.zip')
        zip_path = os.path.join(NLTK_DATA_DIR, 'stopwords.zip')  # Using os.path.join for path compatibility
        
        print(f"Downloading stopwords.zip to {zip_path}...")
        with open(zip_path, 'wb') as download_file:
            data = blob_client.download_blob()
            data.readinto(download_file)

        # Unzip the file
        print("Unzipping stopwords.zip...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(NLTK_DATA_DIR)
    else:
        print("NLTK data directory already exists.")

    # Point NLTK to the right directory
    os.environ['NLTK_DATA'] = NLTK_DATA_DIR
    print(f"NLTK data directory set to: {NLTK_DATA_DIR}")

def download_nltk_resources_to_blob():
    """
    Download NLTK stopwords and store them in Azure Blob Storage.
    """
    TEMP_DIR = '/tmp/nltk_data'  # Temporary path for downloading
    nltk.data.path.append(TEMP_DIR)
    nltk.download('stopwords', download_dir=TEMP_DIR)
    
    # Zip the downloaded data
    with zipfile.ZipFile(os.path.join(TEMP_DIR, 'stopwords.zip'), 'w') as zipf:
        for root, _, files in os.walk(TEMP_DIR):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), TEMP_DIR))
    
    # Upload the zipped file to Azure Blob Storage
    azure_manager.upload_file_to_blob(os.path.join(TEMP_DIR, 'stopwords.zip'), "stopwords.zip")
