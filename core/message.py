import hashlib
import json
from logging import getLogger

import settings
from core.publisher import publish

logger = getLogger(__name__)


class MessagesCombiner:
    """
    union 3 message to 1 message
    set new control sum
    publish to next queue
    """

    def __init__(self):
        self.target_count = 3
        self.current_count = 0
        self.data = ''
        self.queue = 'third'

    def counter(self, ch, method, properties, message) -> None:
        logger.info(f'Got message: {message}')
        self.append(message)
        if self.current_count == self.target_count:
            publish(self.queue, get_message(self.data))
            self.reset()

    def append(self, message) -> None:
        """
        concatenate self.data and message data
        increment self counter
        """
        self.current_count += 1
        self.data += json.loads(message)["data"]

    def reset(self) -> None:
        """
        reset self data and counter values
        """
        self.data = ''
        self.current_count = 0


def get_message(data: str) -> dict[str, str]:
    message = {
        "data": data,
        "control_sum": get_hash(data)
    }
    return message


def get_hash(data: str) -> str:
    """
    :return: hash sum of given string
    """
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))
    return h.hexdigest()
