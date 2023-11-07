import settings
from core.consumer import listen

if __name__ == '__main__':
    listen(settings.RABBITMQ_CONSUME_QUEUE)