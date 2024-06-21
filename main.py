import pika
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    credentials = pika.PlainCredentials('your_username', 'your_password')
    connection_params = pika.ConnectionParameters('localhost', 5672, '/', credentials)

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    queue_name = 'my_queue'
    channel.queue_declare(queue=queue_name, durable=True)

    message = 'Hello, this is a test message!'

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    logger.info(f"Sent '{message}' to queue '{queue_name}'")

    connection.close()
except pika.exceptions.AMQPConnectionError as e:
    logger.error(f"Connection error: {e}")
except pika.exceptions.ChannelError as e:
    logger.error(f"Channel error: {e}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
