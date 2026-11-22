from typing import Any

from bot.core import Handler, HandlerStatus, Messenger


class TextMessageHandler(Handler):
    def __init__(self, messenger: Messenger) -> None:
        self.messenger = messenger

    def handle(self, update: dict[str, Any]) -> HandlerStatus:
        msg = update.get("message", {})
        text = msg.get("text")

        if not text:
            return HandlerStatus.CONTINUE

        self.messenger.send_message(msg["chat"]["id"], text)
        return HandlerStatus.STOP
