from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import logging


storage_account_name = 'cloudshelltechlabvn'
container_name = 'upload'
blob_name = 'upload.txt'
default_credential = DefaultAzureCredential()
account_url=f'https://{storage_account_name}.blob.core.windows.net'
blob_client = BlobServiceClient(account_url=account_url, credential=default_credential)

# Access the specific container
container_client = blob_client.get_container_client(container_name)


try:
    # List all blobs in the container
    logging.info(f"Listing blobs in container: {container_name}")
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print(blob.name)  # Print the blob name
except Exception as e:
    logging.error(f"Failed to list blobs in container {container_name}: {e}")