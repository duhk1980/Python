import logging
import azure.functions as func
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
#any file upload to container named mycontainer
#  get enviroment BLOB_PATH variable from localsetting.json
BLOB_PATH = os.getenv('BLOB_PATH', 'default/path')
@app.blob_trigger(
    arg_name="myblob", path=BLOB_PATH, connection="AzureWebJobsStorage"
)
#trigger from myblog
def blob_trigger (myblob: func.InputStream):
    logging.info(f"Blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    # Process the blob content
    blob_content = myblob.read().decode('utf-8')
    logging.info(f"Blob content: {blob_content}")