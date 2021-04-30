"""
Lock storage
"""
from __future__ import annotations

import logging

from asyncio_lock_manager.sync_primitives.lock import Lock
from .base_storage import SyncPrimitiveStorage
from ..utils.exceptions import CantDeleteWithWaiters


class LockStorage(SyncPrimitiveStorage[Lock]):
    def get_sync_prim(self, key: str) -> Lock:
        return self.sync_prims.setdefault(key, Lock(key))

    def del_sync_prim(self, key: str) -> None:
        lock = self.sync_prims.get(key)
        if not lock:
            logging.warning("Can`t find lock by key to delete %s" % key)
            return
        elif lock and lock.waiters:
            raise CantDeleteWithWaiters("Can`t delete semaphore with waiters %s" % lock)
        else:
            del self.sync_prims[key]
