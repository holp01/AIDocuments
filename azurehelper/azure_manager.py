import base64
import os
from azure.storage.blob import BlobServiceClient
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from pdf_extraction import extractor
import logging

# Azure Blob Storage Configuration
BLOB_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = os.environ.get('BLOB_CONTAINER_NAME')
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)

def cache_content(content, post_id):
    """
    Cache the content in Azure Blob Storage.
    """
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=f"{post_id}.txt")
    blob_client.upload_blob(content, blob_type="BlockBlob", overwrite=True)

def get_cached_content(post_id):
    """
    Retrieve cached content from Azure Blob Storage.
    """
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=f"{post_id}.txt")
    try:
        blob_data = blob_client.download_blob()
        return blob_data.readall().decode('utf-8')
    except Exception as e:
        # Handle the exception (e.g., blob not found)
        return None
    
def cache_content_in_azure(content, arquiTip):
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=f"{arquiTip}.txt")
    blob_client.upload_blob(content, blob_type="BlockBlob", overwrite=True)


def download_and_extract_content_from_azure(arquiTip):
    # Fetch content from Azure Repos
    personal_access_token = os.environ.get('AZURE_DEVOPS_PAT')
    organization_url = os.environ.get('AZURE_DEVOPS_ORG_URL')
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    client = connection.clients.get_git_client()
    file_content_stream = client.get_item_text(repository_id=os.environ.get('AZURE_DEVOPS_REPO_ID'), path=f'content/blog/arqui-tips/{arquiTip}/index.md', project=os.environ.get('AZURE_DEVOPS_PROJECT'))
    
    # Convert generator of bytes to string
    raw_content = ''.join(chunk.decode('utf-8') for chunk in file_content_stream)
    
    # Extract and preprocess content (assuming you have a function for this)
    content = extractor.extract_from_md_content(raw_content)
    
    return arquiTip, content

import requests

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def list_all_md_files():
    personal_access_token = os.environ.get('AZURE_DEVOPS_PAT')
    organization_url = os.environ.get('AZURE_DEVOPS_ORG_URL')
    project_name = os.environ.get('AZURE_DEVOPS_PROJECT')
    repository_id = os.environ.get('AZURE_DEVOPS_REPO_ID')

    # Construct the URL for the REST API endpoint
    api_url = f"{organization_url}/{project_name}/_apis/git/repositories/{repository_id}/items?recursionLevel=full&versionDescriptor[versionType]=branch&versionDescriptor[version]=main&api-version=7.0"

    headers = {
        "Authorization": f"Basic {base64.b64encode((':' + personal_access_token).encode()).decode()}"
    }

    response = requests.get(api_url, headers=headers)
    data = response.json()

    if 'value' not in data:
        logger.error(f"Unexpected response from Azure API: {data}")
        return []

    # Filter paths and extract folder names
    md_files = []
    for item in data['value']:
        if item['path'].startswith('content/blog/arqui-tips/') and item['path'].endswith('index.md'):
            folder_name = item['path'].split('/')[-2]
            md_files.append(folder_name)

    logger.debug(f"Retrieved MD files: {md_files}")
    return md_files

def upload_file_to_blob(file_path, blob_name):
    """
    Upload a file to Azure Blob Storage.
    """
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
