from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class BotError(Exception):
    pass


class HandlerStatus(Enum):
    STOP = "stop"
    CONTINUE = "continue"


class Messenger(ABC):
    @abstractmethod
    def get_updates(self, offset: int, timeout: int) -> list[dict[str, Any]]: ...

    @abstractmethod
    def send_message(self, chat_id: int, text: str) -> None: ...


class Handler(ABC):
    @abstractmethod
    def handle(self, update: dict[str, Any]) -> HandlerStatus: ...
