"""
Lock storage
"""
from __future__ import annotations

import logging

from aiopriman.sync_primitives.lock import Lock
from .base_storage import SyncPrimitiveStorage
from ..utils.exceptions import CantDeleteWithWaiters


class LockStorage(SyncPrimitiveStorage[Lock]):
    prefix = 'Lock:'

    def get_sync_prim(self, key: str) -> Lock:
        return self.sync_prims.setdefault(self.resolve_key(self.prefix, key),
                                          Lock(self.resolve_key(self.prefix, key)))

    def del_sync_prim(self, key: str) -> None:
        lock = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not lock:
            logging.warning("Can`t find lock by key to delete %s" % key)
            return
        elif lock and lock.waiters:
            raise CantDeleteWithWaiters("Can`t delete semaphore with waiters %s" % lock)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
