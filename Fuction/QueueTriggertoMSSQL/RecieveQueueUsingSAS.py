from azure.storage.queue import QueueClient
import os
from urllib.parse import urlparse
import json
import base64

#load local setting.json and set environment, funciton help you create it default
def load_local_settings():
    with open('local.settings.json') as f:
        settings = json.load(f)
    
    # Set environment variables
    for key, value in settings['Values'].items():
        os.environ[key] = value

# Load local settings
load_local_settings()


# Ensure the environment variables are set
if "AZURE_STORAGE_QUEUE_SAS_URL" not in os.environ or "QueueName" not in os.environ or "AzureWebJobsStorage" not in os.environ:
    raise EnvironmentError("Required environment variables are not set")

# Get the SAS URL from the environment variables
sas_url = os.environ["AZURE_STORAGE_QUEUE_SAS_URL"]

# Parse the SAS URL
parsed_url = urlparse(sas_url)
# Extract account_url
account_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.split('/productcatalog')[0]}"
# Extract sas_token
sas_token = parsed_url.query
# Extract the queue name from the URL path (2/)
queue_name = parsed_url.path.split('/')[2]

# Print details to verify
print(f"Account URL: {account_url}")
print(f"SAS Token: {sas_token}")
print(f"Queue Name: {queue_name}")

# Create QueueClient using the SAS token
queue_client = QueueClient(account_url=account_url, queue_name=queue_name, credential=sas_token)

# Example operation: Peek messages from the queue
print("Peeking messages from the queue...")
messages = queue_client.receive_messages()
if not messages:
    print("No messages found in the queue.")
else:
    for message in messages:
        print(f"Message body (encoded): {message.content}")
        try:
            decoded_body = base64.b64decode(message.content).decode('utf-8')
            print(f"Decoded Message Body: {decoded_body}")
        except Exception as e:
            print(f"Error decoding message body: {e}")
