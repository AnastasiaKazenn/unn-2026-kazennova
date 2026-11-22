from typing import Any

from bot.core import Messenger


class LongPolling:
    def __init__(self, messenger: Messenger, timeout: int = 30) -> None:
        self.messenger = messenger
        self.timeout = timeout
        self.offset = 0

    def poll(self) -> list[dict[str, Any]]:
        updates = self.messenger.get_updates(self.offset, self.timeout)
        for u in updates:
            self.offset = max(self.offset, u["update_id"] + 1)
        return updates
