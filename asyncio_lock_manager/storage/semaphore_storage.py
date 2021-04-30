from __future__ import annotations

import logging

from asyncio_lock_manager.sync_primitives.semaphore import Semaphore
from .base_storage import SyncPrimitiveStorage


class SemaphoreStorage(SyncPrimitiveStorage[Semaphore]):
    def get_sync_prim(self, key: str, value=1) -> Semaphore:
        return self.sync_prims.setdefault(key, Semaphore(key, value=value))

    def del_sync_prim(self, key: str) -> None:
        lock = self.sync_prims.get(key)
        if lock and lock.waiters:
            logging.warning("Can`t delete semaphore with waiters %s" % lock)
            return
        try:
            del self.sync_prims[key]
        except KeyError as err:
            logging.warning("Can`t find semaphore by key to delete %s" % err)
