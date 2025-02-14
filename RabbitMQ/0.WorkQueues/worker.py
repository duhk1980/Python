import pika
import time

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



def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    # sent ACK to distributor when procceed message.
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()