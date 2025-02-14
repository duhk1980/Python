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

# Declare the dead-letter exchange
dlx_exchange_name = 'dlx_exchange'
channel.exchange_declare(exchange=dlx_exchange_name, exchange_type='direct')

# Close the connection
connection.close()
