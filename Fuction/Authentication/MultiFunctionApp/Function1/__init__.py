import logging
import azure.functions as func
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Storage account and blob details
        storage_account_name = 'cloudshelltechlabvn'
        container_name = 'upload'
        blob_name = 'upload.txt'

             

        # System-assigned managed identity credential
        credential = ManagedIdentityCredential()

        # Initialize the BlobClient
        blob_client = BlobClient(
        account_url=f'https://{storage_account_name}.blob.core.windows.net',
        credential=credential,
        container_name=container_name,
        blob_name=blob_name
        )

        # Check if the blob exists to validate authentication
        if blob_client.exists():
            return func.HttpResponse("Authentication successful. Blob exists.", status_code=200)
        else:
            return func.HttpResponse("Authentication successful. Blob does not exist.", status_code=200)
    
    except Exception as e:
        # Log and respond with error details
        logging.error(f"Error: {e}")
        return func.HttpResponse(f"Authentication failed or an error occurred: {e}", status_code=500)
