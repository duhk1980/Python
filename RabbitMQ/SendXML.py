import pika
import xml.etree.ElementTree as ET

# Define connection parameters
connection_parameters = pika.ConnectionParameters(
    host='localhost',  # Replace with your RabbitMQ host
    port=5672,         # Replace with your RabbitMQ port if needed
    virtual_host='my_vhost',  # Replace 'myvhost' with the name of your vhost
    credentials=pika.PlainCredentials('guest', 'guest')  # Replace with your RabbitMQ username and password
)

# Establish the connection
connection = pika.BlockingConnection(connection_parameters)
# Create a communication channel
channel = connection.channel()

# Declare the exchange
exchange_name = 'xmlexchange'
exchange_type = 'direct'
channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

# Declare a queue
queue_name = 'XML_queue'
channel.queue_declare(queue=queue_name,durable=True)

# Bind the queue to the exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name)

# Create an XML message with multiple fields
message_content = ET.Element("message")
ET.SubElement(message_content, "title").text = "Hello"
ET.SubElement(message_content, "body").text = "This is an XML message for RabbitMQ"
ET.SubElement(message_content, "timestamp").text = "2025-02-12T20:34:59Z"

# Nested elements
user = ET.SubElement(message_content, "user")
ET.SubElement(user, "name").text = "John Doe"
ET.SubElement(user, "id").text = "12345"
ET.SubElement(user, "email").text = "johndoe@example.com"

xml_message = ET.tostring(message_content, encoding='utf8', method='xml')

# Publish the XML message to the exchange
channel.basic_publish(exchange=exchange_name, routing_key='', body=xml_message)

print('XML message with multiple fields sent to RabbitMQ successfully.')

# Close the connection
connection.close()
