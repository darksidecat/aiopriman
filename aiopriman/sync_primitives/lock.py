"""
Lock synchronization primitive
"""
from __future__ import annotations

import asyncio
from typing import Any, Deque

from .sync_primitive import SyncPrimitive


class Lock(SyncPrimitive):
    """
    Lock synchronization primitive
    """

    def __init__(self, key: str):
        """
        :param key: key
        """
        super().__init__(key)
        self.lock: asyncio.Lock = asyncio.Lock()

    # noinspection PyProtectedMember
    @property
    def waiters(self) -> Deque[asyncio.Future[Any]]:
        """
        :return: waiters
        """
        return self.lock._waiters  # type: ignore

    def __repr__(self) -> str:
        return str("Lock(key={key}, value={lock})".format(key=self.key, lock=self.lock))

    def __str__(self) -> str:
        return self.__repr__()
