from __future__ import annotations

import logging

from asyncio_lock_manager.sync_primitives.semaphore import Semaphore
from .base_storage import SyncPrimitiveStorage
from ..utils.exceptions import CantDeleteWithWaiters


class SemaphoreStorage(SyncPrimitiveStorage[Semaphore]):
    def get_sync_prim(self, key: str, value=1) -> Semaphore:
        return self.sync_prims.setdefault(key, Semaphore(key, value=value))

    def del_sync_prim(self, key: str) -> None:
        sem = self.sync_prims.get(key)
        if not sem:
            logging.warning("Can`t find semaphore by key to delete %s" % key)
            return
        elif sem and sem.waiters:
            raise CantDeleteWithWaiters("Can`t delete semaphore with waiters %s" % sem)
        else:
            del self.sync_prims[key]
