"""
Lock manager
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import BaseManager
from ..storage import LockStorage

if TYPE_CHECKING:  # pragma: no cover
    from aiopriman.sync_primitives.lock import Lock


class LockManager(BaseManager['Lock']):
    """
    Locks manager
    """

    async def __aenter__(self) -> Lock:
        self._current_lock: Lock = self.prim_storage.get_sync_prim(self._key)
        await self._current_lock.lock.acquire()
        return self._current_lock

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._current_lock.lock.release()
        if not self._current_lock.lock.locked() and \
                not self._current_lock.waiters:
            self.prim_storage.del_sync_prim(self._key)

    def resolve_storage(self, storage_data) -> LockStorage:
        return LockStorage(storage_data=storage_data)
