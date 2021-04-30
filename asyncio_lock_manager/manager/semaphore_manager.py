from __future__ import annotations

from typing import TYPE_CHECKING

from . import BaseManager
from ..storage import SemaphoreStorage

if TYPE_CHECKING:  # pragma: no cover
    from asyncio_lock_manager.sync_primitives.semaphore import Semaphore


class SemaphoreManager(BaseManager['Semaphore']):
    async def __aenter__(self) -> Semaphore:
        self._current_sync_prim: Semaphore = self.prim_storage.get_sync_prim(self._key)
        await self._current_sync_prim.sync_prims.acquire()
        return self._current_sync_prim

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._current_sync_prim.sync_prims.release()
        if not self._current_sync_prim.waiters:
            self.prim_storage.del_sync_prim(self._key)

    def resolve_storage(self, storage_data):
        return SemaphoreStorage(storage_data=storage_data)
