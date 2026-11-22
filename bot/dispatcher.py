from typing import Any

from bot.core import Handler, HandlerStatus


class Dispatcher:
    def __init__(self, handlers: list[Handler]) -> None:
        self.handlers = handlers

    def process(self, update: dict[str, Any]) -> None:
        for handler in self.handlers:
            if handler.handle(update) == HandlerStatus.STOP:
                break
