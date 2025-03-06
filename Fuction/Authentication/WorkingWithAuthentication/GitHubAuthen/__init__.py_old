import logging
import os
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.basicConfig(level=logging.INFO)
    # Replace with the client ID of your user-assigned managed identity
    USER_ASSIGNED_CLIENT_ID = os.getenv("USER_ASSIGNED_CLIENT_ID")
    try:
        storage_account_name = 'cloudshelltechlabvn'
        container_name = 'upload'
        #Using system-assigned identity code
        #default_credential = DefaultAzureCredential()
        # Using User-Assigned Identity code
        default_credential = ManagedIdentityCredential(client_id=USER_ASSIGNED_CLIENT_ID)

        account_url=f'https://{storage_account_name}.blob.core.windows.net'
        blob_client = BlobServiceClient(account_url=account_url, credential=default_credential)
        # Access the specific container
        container_client = blob_client.get_container_client(container_name)
        # List all blobs in the container
        logging.info(f"Listing blobs in container: {container_name}")

        # List all blobs in the container
        blob_names = [blob.name for blob in container_client.list_blobs()]
        logging.info(f"Blobs found: {blob_names}")
        return func.HttpResponse(f"Blobs in container '{container_name}': {', '.join(blob_names)}", status_code=200)

    except Exception as e:
        # Log and respond with error details
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Authentication failed or an error occurred: {e}", status_code=500)
