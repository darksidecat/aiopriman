"""
Semaphores storage
"""
from __future__ import annotations

import logging

from aiopriman.sync_primitives.semaphore import Semaphore
from .base_storage import SyncPrimitiveStorage
from ..utils.exceptions import CantDeleteWithWaiters, CantDeleteSemaphoreWithMoreThanOneAcquire


class SemaphoreStorage(SyncPrimitiveStorage[Semaphore]):
    def get_sync_prim(self, key: str, value=1) -> Semaphore:
        """
        Return Semaphore from storage,
        if key not exist in storage then create lock

        :param key: key
        :type key: str
        :param value: Semaphore internal counter, defaults to 1
        :type value: int, optional
        :return: Semaphore
        :rtype: Semaphore
        """
        return self.sync_prims.setdefault(self.resolve_key(self.prefix, key),
                                          Semaphore(self.resolve_key(self.prefix, key),
                                                    value=value))

    def del_sync_prim(self, key: str) -> None:
        """
        Delete semaphore from storage,

        Semaphore with waiters can`t be deleted raise CantDeleteWithWaiters exception
        Semaphore with more than one acquire can`t be deleted
        raise CantDeleteSemaphoreWithMoreThanOneAcquire exception

        if key not found logging this

        :param key: key
        :type key: str
        :return:
        """
        sem = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not sem:
            logging.warning("Can`t find semaphore by key to delete %s" % key)
            return
        elif sem and sem.waiters:
            raise CantDeleteWithWaiters("Can`t delete semaphore with waiters %s" % sem)
        elif sem and sem.value != sem.init_value:
            raise CantDeleteSemaphoreWithMoreThanOneAcquire(
                "Can`t delete semaphore with with more than one current acquire %s" % sem)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
