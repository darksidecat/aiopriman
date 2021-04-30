"""
Lock manager
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import BaseManager
from ..storage import LockStorage

if TYPE_CHECKING:  # pragma: no cover
    from asyncio_lock_manager.sync_primitives.lock import Lock


class LockManager(BaseManager['Lock']):
    async def __aenter__(self) -> Lock:
        self._current_sync_prim: Lock = self.prim_storage.get_sync_prim(self._key)
        await self._current_sync_prim.sync_prims.acquire()
        return self._current_sync_prim

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._current_sync_prim.sync_prims.release()
        if not self._current_sync_prim.waiters:
            self.prim_storage.del_sync_prim(self._key)

    def resolve_storage(self, storage_data):
        return LockStorage(storage_data=storage_data)
