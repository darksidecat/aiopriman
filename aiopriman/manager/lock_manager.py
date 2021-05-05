"""
Lock manager
"""
from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Optional, Type

from . import BaseManager
from ..storage import LockStorage

if TYPE_CHECKING:  # pragma: no cover
    from aiopriman.sync_primitives import Lock
    from ..storage import StorageData


class LockManager(BaseManager['Lock', 'LockStorage']):
    """
    Locks manager
    """

    async def __aenter__(self) -> Lock:
        self._current_lock: Lock = self.prim_storage.get_sync_prim(self._key)
        await self._current_lock.lock.acquire()
        return self._current_lock

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        self._current_lock.lock.release()
        if not self._current_lock.lock.locked() and \
                not self._current_lock.waiters:
            self.prim_storage.del_sync_prim(self._key)

    def resolve_storage(self, storage_data: StorageData[Lock]) -> LockStorage:
        return LockStorage(storage_data=storage_data)
