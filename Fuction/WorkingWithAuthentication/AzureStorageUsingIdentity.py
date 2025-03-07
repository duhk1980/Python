import os
from azure.storage.blob import BlobClient
from azure.identity import ManagedIdentityCredential

# Replace these with your actual values
storage_account_name = 'cloudshelltechlabvn'
container_name = 'upload'
blob_name = 'NewFile'
file_path = 'C:/Users/pc-duhk/temp/Python/Fuction/WorkingWithAuthentication/upload.txt'
user_assigned_client_id = '971ebe17-be69-4fca-81fb-c65a330d1d8e'  # User-assigned managed identity client ID

# Create the BlobClient using the user-assigned managed identity
blob_service_url = f'https://{storage_account_name}.blob.core.windows.net'
credential = ManagedIdentityCredential(client_id=user_assigned_client_id)
blob_client = BlobClient(account_url=blob_service_url, container_name=container_name, blob_name=blob_name, credential=credential)

try:
    # Upload the file
    with open(file_path, 'rb') as file:
        blob_client.upload_blob(file, overwrite=True)
    print(f'File {file_path} uploaded to {container_name}/{blob_name} successfully.')

except Exception as e:
    print(f'Error: {e}')
