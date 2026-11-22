import unittest
from unittest.mock import MagicMock

from bot.core import Handler, HandlerStatus
from bot.dispatcher import Dispatcher


class TestDispatcher(unittest.TestCase):
    def test_stops_on_stop(self) -> None:
        h1 = MagicMock(spec=Handler)
        h1.handle.return_value = HandlerStatus.STOP
        h2 = MagicMock(spec=Handler)

        d = Dispatcher([h1, h2])
        d.process({})

        h1.handle.assert_called_once()
        h2.handle.assert_not_called()
