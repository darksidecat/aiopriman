"""
Lock manager
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from aiopriman.storage import LockStorage

from .base_manager import BaseManager
from .utils import _ContextManagerMixin, inspect_params

if TYPE_CHECKING:  # pragma: no cover
    from aiopriman.storage import StorageData
    from aiopriman.sync_primitives import Lock


class LockManager(BaseManager['Lock', 'LockStorage'], _ContextManagerMixin):
    """
    Locks manager
    """

    def __init__(
            self,
            storage_data: StorageData[Lock],
            key: str = "Default"
    ):
        super().__init__(key=key, storage_data=storage_data)
        self._current_lock: Optional[Lock] = None

    async def acquire(self, *args: Any, **kwargs: Any) -> Lock:
        self._current_lock = self.prim_storage.get_sync_prim(self._key)
        await self._current_lock.lock.acquire()
        return self._current_lock

    def release(self, *args: Any, **kwargs: Any) -> None:
        if not self._current_lock:
            self._current_lock = self.prim_storage.get_sync_prim(self._key)

        try:
            self._current_lock.lock.release()
        finally:
            if (not self._current_lock.lock.locked() and
                    not self._current_lock.waiters):
                self.prim_storage.del_sync_prim(self._key)

    def locked(self) -> bool:
        return self.prim_storage.locked(self._key)

    def resolve_storage(self, storage_data: StorageData[Lock]) -> LockStorage:
        return LockStorage(storage_data=storage_data)
