"""
Lock storage
"""
from __future__ import annotations

import logging

from asyncio_lock_manager.sync_primitives.lock import Lock
from .base_storage import SyncPrimitiveStorage


class LockStorage(SyncPrimitiveStorage[Lock]):
    def get_sync_prim(self, key: str) -> Lock:
        return self.sync_prims.setdefault(key, Lock(key))

    def del_sync_prim(self, key: str) -> None:
        lock = self.sync_prims.get(key)
        if lock and lock.waiters:
            logging.warning("Can`t delete lock with waiters %s" % lock)
            return
        try:
            del self.sync_prims[key]
        except KeyError as err:
            logging.warning("Can`t find lock by key to delete %s" % err)
