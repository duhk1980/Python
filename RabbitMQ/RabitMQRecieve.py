#!/usr/bin/env python
import pika, sys, os
# pika using AMQP 0-9-1


def main():
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
    # create queue 'Hello' if not exist, only one will be created.
    queuename='app1_queue'
    queueroutingkey='app1Key'
    #channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue=queuename, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)