import azure.functions as func
import logging
import os
import requests
from azure.identity import ManagedIdentityCredential, ClientSecretCredential
from azure.storage.blob import BlobClient, BlobServiceClient

app = func.FunctionApp()

@app.route(route="HttpTriggerWithAuthen", auth_level=func.AuthLevel.FUNCTION)
def HttpTriggerWithAuthen(req: func.HttpRequest) -> func.HttpResponse:
    
    # Replace these with your actual values
    #TENANT_ID = "c1c94530-2f83-4e2b-bc0e-94ec42206233"
    #CLIENT_ID = "cb01ef83-1f70-4056-ba49-32bfb4cb724f"
    #CLIENT_SECRET = "80v8Q~h-88fOpAIxbjxDBp2adobpp3SMQnN58bZ-"
    #ACCOUNT_NAME = "cloudshelltechlabvn"
    #CONTAINER_NAME = "upload"

    # Determine if running locally or in the cloud using default information of function
    running_locally = os.getenv('AZURE_FUNCTIONS_ENVIRONMENT') != 'Production'


    TENANT_ID = os.getenv('TENANT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    ACCOUNT_NAME = os.getenv('ACCOUNT_NAME')
    CONTAINER_NAME = os.getenv('CONT_NAME')
    CLIENT_ID = os.getenv('USER_ASSIGNED_CLIENT_ID')
    # Use DefaultAzureCredential for local testing
    if running_locally:
        # if running locally CLIENT_ID= client id of service priciple
        logging.info('Using ClientSecretCredential for local testing.')
        credentials = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
    else:
        # if running cloud CLIENT_ID= client id of user-assigned managed identity
        logging.info('Using ManagedIdentityCredential for cloud deployment.')
        credentials = ManagedIdentityCredential(client_id=CLIENT_ID)

    # Create the BlobClient using the appropriate credentials
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
        logging.info(f'File {file_path} uploaded to {CONTAINER_NAME}/{blob_name} successfully.')

        # List all blobs in the container
        logging.info("\n==============LIST OF ALL BLOBS=================")
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_list = [blob.name for blob in container_client.list_blobs()]
        for blob in blob_list:
            logging.info("\t Blob name: " + blob)

        return func.HttpResponse('Finished execution Function running successfully', status_code=200)
    except Exception as e:
        logging.error(f'Error: {e}')
        return func.HttpResponse(f'Error: {e}', status_code=500)
