import os
import logging
from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy
)

# Configure logging
logging.basicConfig(level=logging.INFO)

def post_xml_to_queue(xml_data: str) -> None:
    try:
        # Retrieve the queue SAS URL from environment variables
        queue_sas_url = "http://127.0.0.1:10001/devstoreaccount1/productcatalog?sv=2020-08-04&st=2025-02-27T00%3A26%3A21Z&se=2025-02-28T00%3A26%3A21Z&sp=rau&sig=xysxkMdEsDRJyowygNHgFyTR%2FrEkv%2FWS7004%2FAbtF%2Fk%3D"
        
        # Create a QueueClient
        queue_client = QueueClient.from_queue_url(queue_sas_url)

        # Setup Base64 encoding and decoding functions
        queue_client.message_encode_policy = BinaryBase64EncodePolicy()
        queue_client.message_decode_policy = BinaryBase64DecodePolicy()

        # Send the XML message to the queue
        message_bytes = xml_data.encode('utf-8')
        encoded_message = queue_client.message_encode_policy.encode(content=message_bytes)
        response = queue_client.send_message(encoded_message)

        # Log the message ID
        logging.info(f"XML message posted to Azure Queue successfully with Message ID: {response.id}")
    
    
    except Exception as e:
        logging.error(f"An error occurred while posting XML message to the queue: {e}")
        
# Main function
if __name__ == "__main__":
    # Example XML data
    xml_data = """
    <root>
        <ProductID>4</ProductID>
        <ProductName>Example Product 4</ProductName>
        <Category>Example Category</Category>
        <Price>20.99</Price>
        <Stock>100</Stock>
    </root>
    """

    # Set environment variables for local execution (optional if already set)
    os.environ['AZURE_STORAGE_QUEUE_SAS_URL'] = "http://127.0.0.1:10001/devstoreaccount1/productcatalog?sv=2020-08-04&st=2025-02-24T01%3A38%3A25Z&se=2025-02-25T01%3A38%3A25Z&sp=rau&sig=jl5v4aLSwjfDDKH8rEuE9dOev1R%2FbPbCIdE%2BejOHJS0%3D"

    # Post the XML message to the queue
    post_xml_to_queue(xml_data)
