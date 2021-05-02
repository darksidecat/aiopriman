import asyncio
from typing import Optional, Deque


from . import SyncPrimitive


class Semaphore(SyncPrimitive[asyncio.Semaphore]):
    def __init__(self, key, value):
        super().__init__(key)
        self.sync_prims: asyncio.Semaphore = asyncio.Semaphore(value)

    # noinspection PyProtectedMember
    @property
    def waiters(self) -> Optional[Deque]:
        return self.sync_prims._waiters  # type: ignore

    def __repr__(self):
        return str({"key": self.key, "sem": self.sync_prims})

    def __str__(self):
        return self.__repr__()
