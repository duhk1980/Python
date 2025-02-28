import logging
import azure.functions as func
import pandas as pd
import os
import xml.etree.ElementTree as ET
from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy,
)

app = func.FunctionApp()

@app.function_name(name="mytimer")
@app.timer_trigger(schedule="0 */1 * * * *", 
              arg_name="mytimer",
              run_on_startup=True) 
def test_function(mytimer: func.TimerRequest) -> None:
    try:
        # Read file path from environment
        blob_file_path = os.getenv('CsvfilePath')
        if blob_file_path is None:
            raise ValueError("CsvfilePath is not set in the environment variables.")
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(blob_file_path)

        # Validate and Transform the DataFrame
        df.dropna(subset=['ProductID', 'ProductName', 'Category', 'Price', 'Stock'], inplace=True)
        
        df['ProductID'] = pd.to_numeric(df['ProductID'], errors='coerce').dropna().astype(int)
        df.drop_duplicates(subset=['ProductID'], inplace=True)
        
        df['ProductName'] = df['ProductName'].astype(str).str.strip()
        df['Category'] = df['Category'].astype(str).str.strip()
        
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df = df[df['Price'] > 0]  # Ensure Price is positive
        
        df['Stock'] = pd.to_numeric(df['Stock'], errors='coerce').dropna().astype(int)
        df = df[df['Stock'] >= 0]  # Ensure Stock is non-negative

        # Setup Connection to Azure Queue
        queue_sas_url = os.getenv('AZURE_STORAGE_QUEUE_SAS_URL') or "http://127.0.0.1:10001/devstoreaccount1/productcatalog?sv=2020-08-04&st=2025-02-24T01%3A38%3A25Z&se=2025-02-25T01%3A38%3A25Z&sp=rau&sig=jl5v4aLSwjfDDKH8rEuE9dOev1R%2FbPbCIdE%2BejOHJS0%3D"
        
        if not queue_sas_url:
            raise ValueError("AZURE_STORAGE_QUEUE_SAS_URL is not set in the environment variables.")

        queue_client = QueueClient.from_queue_url(queue_sas_url)
        queue_client.message_encode_policy = BinaryBase64EncodePolicy()
        queue_client.message_decode_policy = BinaryBase64DecodePolicy()

        # Process each row in the DataFrame
        for index, row in df.iterrows():
            root = ET.Element('Product')
            for field in df.columns:
                field_element = ET.SubElement(root, field)
                field_element.text = str(row[field])
            xml_str = ET.tostring(root, encoding='utf-8', method='xml').decode('utf-8')

            # Encode and send the XML data
            message_bytes = xml_str.encode('utf-8')
            encoded_message = queue_client.message_encode_policy.encode(content=message_bytes)
            queue_client.send_message(encoded_message)
            logging.info(f'Successfully inserted XML for ProductID {row["ProductID"]} into Azure Queue.')

        logging.info('CSV data processed and inserted into Azure Queue successfully.')

    except Exception as e:
        logging.error(f"An error occurred: {e}")
