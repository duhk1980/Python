import logging
import azure.functions as func
import base64
import pyodbc
import xml.etree.ElementTree as ET
from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
import os

def move_to_error_queue(message_content: str, queue_name: str, connection_str: str) -> None:
    try:
        # Create QueueClient for the error queue
        error_queue_client = QueueClient.from_connection_string(conn_str=connection_str, queue_name=queue_name)
        error_queue_client.message_encode_policy = BinaryBase64EncodePolicy()
        error_queue_client.message_decode_policy = BinaryBase64DecodePolicy()
        
        # Encode the message content
        encoded_message = error_queue_client.message_encode_policy.encode(content=message_content.encode('utf-8'))
        
        # Send the message to the error queue and capture the response
        response = error_queue_client.send_message(encoded_message)
        # Extract the message ID from the response
        message_id = response['id']
        logging.info(f"Moved message {message_id} to error queue: {queue_name}")
    except Exception as e:
        logging.error(f"Failed to move message  to error queue: {e}")



# Configure logging
logging.basicConfig(level=logging.INFO)
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="main")
@app.queue_trigger(arg_name="newmessage", queue_name="productcatalog", connection="AzureWebJobsStorage")
def main(newmessage: func.QueueMessage) -> None:
    try:
        # Log the raw message content
        decoded_body = newmessage.get_body().decode('utf-8')
        logging.info(f'Python Queue trigger function processed a queue item: {decoded_body}')
        
        # If the message is XML and not Base64 encoded, process it directly
        logging.info(f"Message body (raw XML): {decoded_body}")

        # Optionally, further processing of the XML message can be done here
        # For example, parsing the XML and extracting specific elements
        
        try:
            root = ET.fromstring(decoded_body)
            logging.debug(f'Parsed XML Root: {ET.tostring(root, encoding="utf-8").decode("utf-8")}')
            
            # Initialize data list
            data = []
            
            # Create a record dictionary
            record = {}
            
            # Iterate through child elements
            for child in root:
                record[child.tag] = child.text
                print(f'{child.tag}: {child.text}')  # Print child tag and text
            
            # Append the record to the data list
            data.append(record)
            
            # Log and print the final data
            logging.info(f'Converted XML message to dictionary: {data}')
            #print(f'Converted XML message to dictionary: {data}')
            
                
            # Validate data
            for record in data:
                if not all([record.get('ProductID'), record.get('ProductName'), record.get('Category'), record.get('Price'), record.get('Stock')]):
                    logging.error(f"Missing fields in record: {record}")
                # return

            # Establish SQL Server connection
            server= os.getenv('dbserver')
            database = os.getenv('database')
            driver = os.getenv('driver')
            ErrorQueueName=os.getenv('ErrorQueueName')
            QueueConnectionStr=os.getenv('AzureWebJobsStorage')
            # Log the parameters
            try:
                # connect to database
                conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
                cursor = conn.cursor()
                logging.info('Database connection established successfully.')
                # Insert data into SQL database
                for record in data:
                    try:
                        cursor.execute("""
                            INSERT INTO ProductCatalog (ProductID, ProductName, Category, Price, Stock)
                            VALUES (?, ?, ?, ?, ?)
                        """, int(record['ProductID']), record['ProductName'], record['Category'], float(record['Price']), int(record['Stock']))
                        logging.info(f'Successfully inserted record: {record}')

                        
                    except Exception as e:
                        logging.error(f"Error inserting record {record}: {e}")
                        #moving to error queue to investigating later
                        move_to_error_queue(decoded_body, ErrorQueueName, QueueConnectionStr)
                        break  # Break the loop if duplicate found
                #Commit transaction
                conn.commit()
            except pyodbc.Error as e:
                # Log the error if connection fails
                logging.error(f'Error connecting to the database: {e}')
        except ET.ParseError as e:
            logging.error(f'Error while parsing XML: {e}')
            move_to_error_queue(decoded_body, ErrorQueueName, QueueConnectionStr)

    except Exception as e:
        logging.error(f"Error processing message body: {e}")
        move_to_error_queue(decoded_body, ErrorQueueName, QueueConnectionStr)

