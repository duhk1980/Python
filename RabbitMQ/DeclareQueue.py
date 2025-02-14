# Declare a queue with dead letter and config dead letter forward message to Dead letter queue to review and analysic later.
import pika

# Define connection parameters with a specific port and vhost
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

# Declare the original queue with dead-letter exchange argument
original_queue_name = 'app1_queue'
arguments = {
    #'x-expires': 60000,         # Queue expires after 60 seconds of inactivity it will be deleted
    'x-message-ttl': 30000,     # Messages expire after 30 seconds in the queue
    'x-max-length': 1000,       # Maximum number of messages the queue can hold
    'x-dead-letter-exchange': 'dlx_exchange'  # Dead-letter exchange for rejected/expired messages
}
channel.queue_declare(queue=original_queue_name, durable=True, arguments=arguments)

# Declare Exchage and Bind the original queue to the main exchange (e.g., 'my_exchange')
main_exchange_name = 'app1_exchange'
app1_routing_key = 'app1Key'
channel.exchange_declare(exchange=main_exchange_name,durable=True, exchange_type='direct')
channel.queue_bind(exchange=main_exchange_name, queue=original_queue_name, routing_key=app1_routing_key)

print('Queue declared and bound to exchange with arguments successfully.')

# Close the connection
connection.close()
