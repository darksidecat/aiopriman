"""
Locks storage
"""
from __future__ import annotations

import logging

from aiopriman.sync_primitives import Lock
from aiopriman.utils.exceptions import CantDeleteWithWaiters

from .base_storage import BaseStorage

logger = logging.getLogger(__name__)


class LockStorage(BaseStorage[Lock]):
    def get_sync_prim(self, key: str) -> Lock:
        """
        Return Lock from storage,
        if key not exist in storage then create lock

        :param key: key
        :return: Lock
        """
        return self.sync_prims.setdefault(self.resolve_key(self.prefix, key),
                                          Lock(self.resolve_key(self.prefix, key)))

    def del_sync_prim(self, key: str) -> None:
        """
        Delete lock from storage,

        raise CantDeleteWithWaiters exception

        if key not found logging this

        :param key: key
        :return:
        """
        lock = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not lock:
            logger.warning("Can`t find Lock by key to delete %s" % key)
            return
        elif lock and lock.waiters:
            raise CantDeleteWithWaiters("Can`t delete Lock with waiters %s" % lock)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
