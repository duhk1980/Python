import pika
import sys

# Define connection parameters with a specific port and vhost
connection_parameters = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    virtual_host='my_vhost',
    credentials=pika.PlainCredentials('guest', 'guest')
)

# Establish the connection
connection = pika.BlockingConnection(connection_parameters)

# Create a communication channel
channel = connection.channel()

# Declare the queue if it does not exist
queue_name = 'app1_queue'
exchangename='app1_exchange'
queueroutingkey='app1Key'
#MessageBody='Hello word'
#channel.queue_declare(queue=queue_name, durable=True)


message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange=exchangename,
    routing_key=queueroutingkey,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    ))
print(f" [x] Sent {message}")
connection.close()
