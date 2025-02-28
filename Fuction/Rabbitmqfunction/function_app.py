import azure.functions as func
import datetime
import json
import logging
import pika

app = func.FunctionApp()

@app.route(route="HttpToRabbitMQ", auth_level=func.AuthLevel.ANONYMOUS)
def HttpToRabbitMQ(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Read the message from the HTTP request
    message = req.get_json().get('message')

    if not message:
        return func.HttpResponse(
            "Please pass a message in the request body",
            status_code=400
        )
    if message:
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
        
        # Declare a queue (if it doesn't exist)
        queue_name = 'myqueue'
        channel.queue_declare(queue=queue_name)

        # Publish the message to the queue
        channel.basic_publish(exchange='',
                            routing_key=queue_name,
                            body=message)

        # Close the connection
        connection.close()

        return func.HttpResponse(
            f"Message '{message}' sent to RabbitMQ queue '{queue_name}'",
            status_code=200
        )
        