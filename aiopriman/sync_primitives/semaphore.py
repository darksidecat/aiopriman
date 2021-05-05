"""
Semaphore synchronization primitive
"""
from __future__ import annotations

import asyncio
from typing import Deque, Any, TYPE_CHECKING

from . import SyncPrimitive

if TYPE_CHECKING:  # pragma: no cover
    from asyncio import Future


# noinspection PyProtectedMember
class Semaphore(SyncPrimitive[asyncio.Semaphore]):
    """
    Semaphore synchronization primitive
    """

    def __init__(self, key: str, value: int = 1):
        """
        :param key: key
        :type key: str
        :param value: Semaphore internal counter, defaults to 1
        :type value: int, optional
        """
        super().__init__(key)
        self.init_value = value
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(value)

    @property
    def waiters(self) -> Deque[Future[Any]]:
        """
        :return: waiters
        :rtype: Deque[Future[Any]]
        """
        return self.semaphore._waiters

    @property
    def value(self) -> int:
        return self.semaphore._value

    def __repr__(self) -> str:
        return str("Semaphore(key={key}, value={sem})".format(
            key=self.key,
            sem=self.semaphore)
        )

    def __str__(self) -> str:
        return self.__repr__()
