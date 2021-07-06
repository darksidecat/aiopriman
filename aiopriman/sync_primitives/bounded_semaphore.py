"""
Semaphore synchronization primitive
"""
from __future__ import annotations

import asyncio
from typing import Any, Deque

from .sync_primitive import SyncPrimitive


# noinspection PyProtectedMember
class BoundedSemaphore(SyncPrimitive):
    """
    BoundedSemaphore synchronization primitive
    """

    def __init__(self, key: str, value: int = 1):
        """
        :param key: key
        :param value: BoundedSemaphore internal counter, defaults to 1
        """
        super().__init__(key)
        self.init_value = value
        self.pending = 0  # counter for SemaphoreManager
        self.semaphore: asyncio.Semaphore = asyncio.BoundedSemaphore(value)

    @property
    def waiters(self) -> Deque[asyncio.Future[Any]]:
        """
        :return: waiters
        """
        return self.semaphore._waiters

    @property
    def value(self) -> int:
        return self.semaphore._value

    def __repr__(self) -> str:
        return str(
            "BoundedSemaphore(key={key}, value={sem}, pending={pending})".format(
                key=self.key,
                sem=self.semaphore,
                pending=self.pending,
            )
        )

    def __str__(self) -> str:
        return self.__repr__()
