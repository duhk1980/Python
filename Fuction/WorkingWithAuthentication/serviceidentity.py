import logging
import os
import requests
from azure.identity import ClientSecretCredential
import azure.functions as func
from azure.storage.blob import BlobClient, BlobServiceClient

# Tenant ID for your Azure Subscription
TENANT_ID = "c1c94530-2f83-4e2b-bc0e-94ec42206233"

# Your Service Principal App ID (Client ID)
CLIENT_ID = "cb01ef83-1f70-4056-ba49-32bfb4cb724f"

# Your Service Principal Password (Client Secret)
CLIENT_SECRET = "80v8Q~h-88fOpAIxbjxDBp2adobpp3SMQnN58bZ-"

ACCOUNT_NAME = "cloudshelltechlabvn"
CONTAINER_NAME = "upload"

# Initialize the credentials and BlobServiceClient
credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
blob_service_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net"
blob_service_client = BlobServiceClient(blob_service_url, credential=credentials)

# Create a BlobClient
blob_name = 'NewFile'
file_path = 'C:/Users/pc-duhk/temp/Python/Fuction/WorkingWithAuthentication/upload.txt'
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)

# Upload the file
try:
    with open(file_path, 'rb') as file:
        blob_client.upload_blob(file, overwrite=True)
    print(f'File {file_path} uploaded to {CONTAINER_NAME}/{blob_name} successfully.')
except Exception as e:
    print(f'Error: {e}')
    func.HttpResponse(f'Error: {e}', status_code=500)

print("\n==============LIST OF ALL BLOBS=================")

# List all blobs in the container
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
for blob in container_client.list_blobs():
    print("\t Blob name: " + blob.name)

func.HttpResponse('Finished execution', status_code=200)
