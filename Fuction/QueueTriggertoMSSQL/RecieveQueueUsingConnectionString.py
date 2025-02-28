from azure.storage.queue import QueueServiceClient, QueueClient
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
#sas_url = os.environ["AZURE_STORAGE_QUEUE_SAS_URL"]
queue_name = os.environ["QueueName"]
conn_str = os.environ["AzureWebJobsStorage"]



# Create QueueClient using connection string
queue_client = QueueClient.from_connection_string(conn_str=conn_str, queue_name=queue_name)

# Print details to verify
print(f"Queue Name: {queue_name}")

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
