"""
Conditions storage
"""
from __future__ import annotations

import logging
from typing import Optional

from aiopriman.sync_primitives import Condition
from aiopriman.utils.exceptions import CantDeleteWithWaiters

from .base_storage import BaseStorage

logger = logging.getLogger(__name__)


class ConditionStorage(BaseStorage[Condition]):
    def locked(self, key: str) -> bool:
        condition: Optional[Condition] = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if condition and condition.condition.locked():
            return True
        return False

    def get_sync_prim(self, key: str) -> Condition:
        """
        Return Condition from storage,
        if key not exist in storage then create condition

        :param key: key
        :return: Condition
        """
        return self.sync_prims.setdefault(
            self.resolve_key(self.prefix, key), Condition(self.resolve_key(self.prefix, key))
        )

    def del_sync_prim(self, key: str) -> None:
        """
        Delete condition from storage,

        raise CantDeleteWithWaiters exception

        if key not found logging this

        :param key: key
        :return:
        """
        condition = self.sync_prims.get(self.resolve_key(self.prefix, key))
        if not condition:
            logger.warning("Can`t find Condition by key to delete %s" % key)
        elif condition.waiters:
            raise CantDeleteWithWaiters("Can`t delete Condition with waiters %s" % condition)
        else:
            del self.sync_prims[self.resolve_key(self.prefix, key)]
