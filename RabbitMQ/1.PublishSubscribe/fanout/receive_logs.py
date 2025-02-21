#!/usr/bin/env python
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

channel = connection.channel()
# Declare Channel Fanout if not exist.

channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Declare queue with randomename from system
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

#bind to exchange log
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

# Process message

def callback(ch, method, properties, body):
    print(f" [x] {body}")

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()