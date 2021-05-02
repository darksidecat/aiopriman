"""
Locks storage
"""
from __future__ import annotations

import logging

from aiopriman.sync_primitives.lock import Lock
from .base_storage import SyncPrimitiveStorage
from ..utils.exceptions import CantDeleteWithWaiters


class LockStorage(SyncPrimitiveStorage[Lock]):
    def get_sync_prim(self, key: str) -> Lock:
        """
        Return Lock from storage,
        if key not exist in storage then create lock

        :param key: key
        :type key: str
        :return: Lock
        :rtype: Lock
        """
        return self.sync_prims.setdefault(self.resolve_key(self.prefix, key),
                                          Lock(self.resolve_key(self.prefix, key)))

    def del_sync_prim(self, key: str) -> None:
        """
        Delete lock from storage,
        if key can`t be deleted raise CantDeleteWithWaiters exception
        if key not found logging this

        :param key: key
        :type key: str
        :return:
        """
        lock = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not lock:
            logging.warning("Can`t find lock by key to delete %s" % key)
            return
        elif lock and lock.waiters:
            raise CantDeleteWithWaiters("Can`t delete lock with waiters %s" % lock)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
