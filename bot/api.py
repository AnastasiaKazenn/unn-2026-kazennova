import json
import logging
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, cast

from bot.core import BotError, Messenger

logger = logging.getLogger(__name__)


class TelegramAPI(Messenger):
    def __init__(self) -> None:
        raw_base = os.environ.get("TELEGRAM_BASE_URL", "").strip()
        if raw_base and not raw_base.startswith(("http://", "https://")):
            raw_base = "https://" + raw_base

        if "localhost" in raw_base or "127.0.0.1" in raw_base:
            raw_base = raw_base.replace("localhost", "172.17.0.1").replace(
                "127.0.0.1", "172.17.0.1"
            )

        self.base_url = raw_base.rstrip("/")
        self.token = os.environ["TELEGRAM_TOKEN"]

    def _call(self, method: str, **kwargs: Any) -> Any:
        url = f"{self.base_url}/bot{self.token}/{method}"

        poll_timeout = kwargs.get("timeout", 10)
        socket_timeout = (poll_timeout + 15) if isinstance(poll_timeout, int) else 30
        ctx = ssl._create_unverified_context()

        req = urllib.request.Request(
            url, data=urllib.parse.urlencode(kwargs).encode(), method="POST"
        )

        logger.debug("Request to %s", method)

        try:
            with urllib.request.urlopen(
                req, timeout=socket_timeout, context=ctx
            ) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            data = json.loads(e.read())
            if not data.get("ok"):
                raise BotError(f"API Error: {data.get('description')}") from e
            return data["result"]
        except urllib.error.URLError as e:
            raise BotError(f"Network error: {e.reason}") from e

        if not data.get("ok"):
            raise BotError(f"API Error: {data.get('description')}")

        return data["result"]

    def get_updates(self, offset: int, timeout: int) -> list[dict[str, Any]]:
        result = self._call(
            "getUpdates",
            offset=offset,
            timeout=timeout,
            limit=100,
            allowed_updates=json.dumps(["message"]),
        )
        return cast(list[dict[str, Any]], result)

    def send_message(self, chat_id: int, text: str) -> None:
        self._call("sendMessage", chat_id=chat_id, text=text)
