"""
BoundedSemaphores storage
"""
from __future__ import annotations

import logging
from typing import Optional

from aiopriman.sync_primitives import BoundedSemaphore
from aiopriman.utils.exceptions import (CantDeleteSemaphoreWithAcquire,
                                        CantDeleteWithWaiters)

from .base_storage import BaseStorage

logger = logging.getLogger(__name__)


class BoundSemaphoreStorage(BaseStorage[BoundedSemaphore]):
    def locked(self, key: str) -> bool:
        sem: Optional[BoundedSemaphore] = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if sem and sem.semaphore.locked():
            return True
        return False

    def get_sync_prim(self, key: str, value: int = 1) -> BoundedSemaphore:
        """
        Return BoundedSemaphore from storage,
        if key not exist in storage then create BoundedSemaphore

        :param key: key
        :param value: BoundedSemaphore internal counter, defaults to 1
        :return: BoundedSemaphore
        """
        return self.sync_prims.setdefault(
            self.resolve_key(self.prefix, key),
            BoundedSemaphore(self.resolve_key(self.prefix, key), value=value)
        )

    def del_sync_prim(self, key: str) -> None:
        """
        Delete BoundedSemaphore from storage,

        raise CantDeleteWithWaiters exception
        raise CantDeleteSemaphoreWithAcquire exception

        if key not found logging this

        :param key: key
        :return:
        """
        sem = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not sem:
            logger.warning("Can`t find BoundedSemaphore by key to delete %s" % key)
            return
        elif sem and sem.waiters:
            raise CantDeleteWithWaiters("Can`t delete BoundedSemaphore with waiters %s" % sem)
        elif sem and sem.value != sem.init_value:
            raise CantDeleteSemaphoreWithAcquire(
                "Can`t delete BoundedSemaphore with acquire %s" % sem)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
