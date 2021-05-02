"""
Lock synchronization primitive
"""
import asyncio
from typing import Optional, Deque

from . import SyncPrimitive


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
    def waiters(self) -> Optional[Deque]:
        """
        :return: waiters
        :rtype: Optional[Deque]
        """
        return self.lock._waiters  # type: ignore

    def __repr__(self):
        return str("Lock(key={key}, value={lock})".format(
            key=self.key,
            lock=self.lock)
        )

    def __str__(self):
        return self.__repr__()
