import pika
# pika using AMQP 0-9-1

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
# create queue Hello
queuename='app1_queue'
exchangename='app1_exchange'
queueroutingkey='app1Key'
MessageBody='Hello word'
#channel.queue_declare(queue=queuename,durable=True)
# push message to queue hello
channel.basic_publish(exchange=exchangename, routing_key=queueroutingkey, body=MessageBody)
print(" [x] Sent "+MessageBody)
connection.close()