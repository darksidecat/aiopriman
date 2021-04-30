"""
Lock synchronization primitive
"""
import asyncio
from typing import Optional, Deque

from . import SyncPrimitive


class Lock(SyncPrimitive[asyncio.Lock]):
    def __init__(self, key: str):
        super().__init__(key)
        self.sync_prims: asyncio.Lock = asyncio.Lock()

    # noinspection PyProtectedMember
    @property
    def waiters(self) -> Optional[Deque]:
        return self.sync_prims._waiters  # type: ignore

    def __repr__(self):
        return str({"key": self.key, "lock": self.sync_prims})

    def __str__(self):
        return self.__repr__()
