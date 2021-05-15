"""
Semaphores storage
"""
from __future__ import annotations

import logging

from aiopriman.sync_primitives import Semaphore
from aiopriman.utils.exceptions import (CantDeleteSemaphoreWithAcquire,
                                        CantDeleteWithWaiters)

from .base_storage import BaseStorage

logger = logging.getLogger(__name__)


class SemaphoreStorage(BaseStorage[Semaphore]):
    def get_sync_prim(self, key: str, value: int = 1) -> Semaphore:
        """
        Return Semaphore from storage,
        if key not exist in storage then create Semaphore

        :param key: key
        :param value: Semaphore internal counter, defaults to 1
        :return: Semaphore
        """
        return self.sync_prims.setdefault(self.resolve_key(self.prefix, key),
                                          Semaphore(self.resolve_key(self.prefix, key),
                                                    value=value))

    def del_sync_prim(self, key: str) -> None:
        """
        Delete semaphore from storage,

        raise CantDeleteWithWaiters exception
        raise CantDeleteSemaphoreWithAcquire exception

        if key not found logging this

        :param key: key
        :return:
        """
        sem = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not sem:
            logger.warning("Can`t find Semaphore by key to delete %s" % key)
            return
        elif sem and sem.waiters:
            raise CantDeleteWithWaiters("Can`t delete Semaphore with waiters %s" % sem)
        elif sem and sem.value != sem.init_value:
            raise CantDeleteSemaphoreWithAcquire(
                "Can`t delete Semaphore with acquire %s" % sem)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
