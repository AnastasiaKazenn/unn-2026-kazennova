import unittest
from unittest.mock import MagicMock

from bot.core import HandlerStatus
from bot.handlers import TextMessageHandler


class TestTextMessageHandler(unittest.TestCase):
    def test_echo_text(self) -> None:
        messenger = MagicMock()
        handler = TextMessageHandler(messenger)
        update = {"message": {"text": "Hi", "chat": {"id": 42}}}

        status = handler.handle(update)

        self.assertEqual(status, HandlerStatus.STOP)
        messenger.send_message.assert_called_once_with(42, "Hi")
