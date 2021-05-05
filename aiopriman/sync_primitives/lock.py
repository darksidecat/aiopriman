"""
Lock synchronization primitive
"""
from __future__ import annotations

import asyncio
from typing import Any, Deque, TYPE_CHECKING

from . import SyncPrimitive

if TYPE_CHECKING:  # pragma: no cover
    from asyncio import Future


class Lock(SyncPrimitive[asyncio.Lock]):
    """
    Lock synchronization primitive
    """

    def __init__(self, key: str):
        """
        :param key: key
        :type key: str
        """
        super().__init__(key)
        self.lock: asyncio.Lock = asyncio.Lock()

    # noinspection PyProtectedMember
    @property
    def waiters(self) -> Deque[Future[Any]]:
        """
        :return: waiters
        :rtype:Deque[Future[Any]]
        """
        return self.lock._waiters  # type: ignore

    def __repr__(self) -> str:
        return str("Lock(key={key}, value={lock})".format(
            key=self.key,
            lock=self.lock)
        )

    def __str__(self) -> str:
        return self.__repr__()
