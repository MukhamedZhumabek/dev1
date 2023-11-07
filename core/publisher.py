import json
from logging import getLogger

import pika

import settings

logger = getLogger(__name__)

credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)


def publish(queue, message):
    params = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
    logger.info(f"publish {message}")
    connection.close()
