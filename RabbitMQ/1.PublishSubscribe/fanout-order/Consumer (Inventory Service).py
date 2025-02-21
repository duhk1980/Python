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
channel = connection.channel()

# Declare a fanout exchange if not exist.
channel.exchange_declare(exchange='order_exchange', exchange_type='fanout')

# Declare a queue and bind it to the exchange
queue_name = 'inventory_queue'
channel.queue_declare(queue=queue_name)
channel.queue_bind(exchange='order_exchange', queue=queue_name)

# Callback function to process messages
def callback(ch, method, properties, body):
    order = json.loads(body)
    order_id = order['order_id']
    item = order['item']
    quantity = order['quantity']
    print(f" [x] Inventory Service received order {order_id}: {item} (quantity: {quantity})")
    # Process inventory update here

# Start consuming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
