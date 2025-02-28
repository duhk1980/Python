import xml.etree.ElementTree as ET
import logging
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage
import base64
import pyodbc
# Configure logging
logging.basicConfig(level=logging.DEBUG)

# 1. Define Connection to Azurite
connect_str = "AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;DefaultEndpointsProtocol=http;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
queue_name = "productcatalog"

# 2. Create a QueueClient and Get Messages
queue_client = QueueClient.from_connection_string(connect_str, queue_name)
messages = queue_client.receive_messages(messages_per_page=10)

# 3. Process messages
for msg in messages:
    message_body = msg.content  # Get the message body
    # Decode the Base64 encoded message body because azurequeu enscrypted using Base64
    decoded_body = base64.b64decode(message_body).decode('utf-8')
    
    # Log the decoded message body
    logging.debug(f'Decoded Message Body: {decoded_body}')
    
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
        print(f'Converted XML message to dictionary: {data}')
        
        # Delete the message after processing
        queue_client.delete_message(msg)
        # Validate data
        for record in data:
            if not all([record.get('ProductID'), record.get('ProductName'), record.get('Category'), record.get('Price'), record.get('Stock')]):
                logging.error(f"Missing fields in record: {record}")
               # return
        # Establish SQL Server connection
        server = 'localhost\\SQLEXPRESS'
        database = 'RetailDB'
        driver = '{ODBC Driver 17 for SQL Server}'
        # Configure logging
        logging.basicConfig(filename='database_connection.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        try:
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
            conn.commit()
            logging.info('Message processed and data inserted into SQL database.')
        except pyodbc.Error as e:
            # Log the error if connection fails
            logging.error(f'Error connecting to the database: {e}')

    except ET.ParseError as e:
        logging.error(f'Error while parsing XML: {e}')
        print(f'Error while parsing XML: {e}')
    