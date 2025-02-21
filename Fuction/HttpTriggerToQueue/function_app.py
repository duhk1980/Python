import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import logging
from azure.core.exceptions import ResourceExistsError
# to create randome code
import uuid

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="Httptoqueue")

def Httptoqueue(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Read the file content from the HTTP request
    file_content = req.get_body()
    
    # Define the connection string and container name
    
    #connect_str = "DefaultEndpointsProtocol=https;AccountName=youraccountname;AccountKey=youraccountkey;EndpointSuffix=core.windows.net"
    container_name = "mycontainer"
    connect_str ="AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
    #connect_str = "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
    # Create BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    # Create a container client
    container_client = blob_service_client.get_container_client(container_name)
    
    # Create the container if it doesn't exist
    try:
        container_client.create_container()
        logging.info(f"Container '{container_name}' created successfully.")
    except ResourceExistsError:
        logging.info(f"Container '{container_name}' already exists.")
       
    # Create a blob client using the local file name as the name for the blob
    # Generate a unique blob name
    unique_blob_name = f"{uuid.uuid4()}_example.txt"
    blob_client = container_client.get_blob_client(unique_blob_name)
    
    # Upload the file to the blob
    # Check if the blob exists
    if not blob_client.exists():
        # Upload the file to the blob
        blob_client.upload_blob(file_content)
        logging.info(f"Blob '{unique_blob_name}' uploaded successfully.")
    
    return func.HttpResponse(
        f"Blob '{unique_blob_name}' uploaded successfully.",
        status_code=200
    )
