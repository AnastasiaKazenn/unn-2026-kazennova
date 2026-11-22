import unittest
from unittest.mock import MagicMock, patch

from bot.api import TelegramAPI


class TestTelegramAPI(unittest.TestCase):
    @patch.dict(
        "os.environ", {"TELEGRAM_BASE_URL": "http://test", "TELEGRAM_TOKEN": "123"}
    )
    @patch("urllib.request.urlopen")
    def test_get_updates_limit(self, mock_urlopen: MagicMock) -> None:
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"ok": true, "result": []}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        api = TelegramAPI()
        api.get_updates(0, 30)

        req = mock_urlopen.call_args.args[0]
        self.assertIn(b"limit=100", req.data)
