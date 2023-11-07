from logging import getLogger

import pika

import settings

from core.message import MessagesCombiner

logger = getLogger(__name__)

credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
combiner = MessagesCombiner()


def listen(queue):
    params = pika.ConnectionParameters(host=settings.RABBITMQ_HOST, credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_consume(queue=queue, on_message_callback=combiner.counter, auto_ack=True)
    logger.info("Consumer waiting for messages...")
    channel.start_consuming()
