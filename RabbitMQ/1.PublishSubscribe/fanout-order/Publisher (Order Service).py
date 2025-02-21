import pika
import json

# Define connection parameters with a specific port and vhost
connection_parameters = pika.ConnectionParameters(
    host='localhost',  # Replace with your RabbitMQ host
    port=5672,         # Replace with your RabbitMQ port if needed
    virtual_host='order_service',  # Replace 'myvhost' with the name of your vhost
    credentials=pika.PlainCredentials('guest', 'guest')  # Replace with your RabbitMQ username and password
)

# Establish the connection
connection = pika.BlockingConnection(connection_parameters)

# Create a communication channel
channel = connection.channel()

# Declare a fanout exchange
channel.exchange_declare(exchange='order_exchange', exchange_type='fanout')

# Create an order message as a dictionary
order_message = {
    'order_id': '123',
    'item': 'Widget',
    'quantity': 2,
    'customer_email': 'duhk1980@gmail.com'
}

# Convert the order message to JSON format
order_message_json = json.dumps(order_message)

# Publish order message

channel.basic_publish(exchange='order_exchange', routing_key='', body=order_message_json)

print(f" [x] Sent '{order_message_json}'")

# Close connection
connection.close()
