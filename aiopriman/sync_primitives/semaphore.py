"""
Semaphore synchronization primitive
"""
import asyncio
from typing import Optional, Deque

from . import SyncPrimitive


# noinspection PyProtectedMember
class Semaphore(SyncPrimitive[asyncio.Semaphore]):
    """
    Semaphore synchronization primitive
    """

    def __init__(self, key, value):
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
    def waiters(self) -> Optional[Deque]:
        """
        :return: waiters
        :rtype: Optional[Deque]
        """
        return self.semaphore._waiters  # type: ignore

    @property
    def value(self) -> int:
        return self.semaphore._value  # type: ignore

    def __repr__(self):
        return str("Semaphore(key={key}, value={sem})".format(
            key=self.key,
            sem=self.semaphore)
        )

    def __str__(self):
        return self.__repr__()
