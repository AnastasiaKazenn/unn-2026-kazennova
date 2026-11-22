import logging
import time
import urllib.error

from bot.api import TelegramAPI
from bot.core import BotError, Handler
from bot.dispatcher import Dispatcher
from bot.handlers import TextMessageHandler
from bot.polling import LongPolling

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting bot...")
    api = TelegramAPI()
    polling = LongPolling(api)

    handlers: list[Handler] = [TextMessageHandler(api)]
    dispatcher = Dispatcher(handlers)

    while True:
        try:
            updates = polling.poll()
            for update in updates:
                dispatcher.process(update)
        except BotError as e:
            logger.error("Bot API error: %s", e)
            time.sleep(1)
        except (urllib.error.URLError, TimeoutError) as e:
            logger.error("Network/Timeout error: %s", e)
            time.sleep(1)


if __name__ == "__main__":
    main()
