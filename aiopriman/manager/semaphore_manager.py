"""
Semaphore manager
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from . import BaseManager
from ..storage import SemaphoreStorage

if TYPE_CHECKING:  # pragma: no cover
    from aiopriman.sync_primitives.semaphore import Semaphore
    from aiopriman.storage.base_storage import StorageData


class SemaphoreManager(BaseManager['Semaphore', 'SemaphoreStorage']):
    """
    Semaphore manager
    """

    def __init__(self,
                 key: str = None,
                 storage_data: StorageData = None,
                 value: int = 1):
        """
        :param key: Key for managing semaphore
        :type key: str
        :param storage_data: StorageData
        :type storage_data: StorageData, optional
        :param value: Semaphore internal counter, defaults to 1
        :type value: int, optional
        """
        super().__init__(key=key, storage_data=storage_data)
        self.value = value

    async def __aenter__(self) -> Semaphore:
        self._current_semaphore: Semaphore = self.prim_storage.get_sync_prim(
            key=self._key,
            value=self.value
        )
        await self._current_semaphore.semaphore.acquire()
        return self._current_semaphore

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Check waiters before release for not deleting key too early
        waiters_before_release = bool(self._current_semaphore.waiters)

        # In case when Semaphore released more times than acquired
        if self.value == self._current_semaphore.value:
            self.value += 1
            self._current_semaphore.init_value += 1

        self._current_semaphore.semaphore.release()

        if not self._current_semaphore.semaphore.locked() and \
                not self._current_semaphore.waiters and \
                not waiters_before_release and \
                self._current_semaphore.value == self.value:
            self.prim_storage.del_sync_prim(self._key)

    def resolve_storage(self, storage_data) -> SemaphoreStorage:
        return SemaphoreStorage(storage_data=storage_data)
