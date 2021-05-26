"""
Semaphore manager
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from aiopriman.storage import SemaphoreStorage

from .base_manager import BaseManager
from .utils import _ContextManagerMixin

if TYPE_CHECKING:  # pragma: no cover
    from aiopriman.storage import StorageData
    from aiopriman.sync_primitives import Semaphore


class SemaphoreManager(BaseManager['Semaphore', 'SemaphoreStorage'], _ContextManagerMixin):
    """
    Semaphores manager
    """

    def __init__(
            self,
            storage_data: StorageData[Semaphore],
            key: str = "Default",
            value: int = 1
    ):
        """
        :param key: Key for managing Semaphore
        :param storage_data: StorageData
        :param value: Semaphore internal counter, defaults to 1
        """
        super().__init__(key=key, storage_data=storage_data)
        self.value = value
        self._current_semaphore: Optional[Semaphore] = None

    async def acquire(self, from_context_manager: bool = False) -> Semaphore:
        self._current_semaphore = self.prim_storage.get_sync_prim(
            key=self._key,
            value=self.value
        )
        self._current_semaphore.pending += 1
        await self._current_semaphore.semaphore.acquire()
        return self._current_semaphore

    def release(self, from_context_manager: bool = False) -> None:
        if not self._current_semaphore:
            self._current_semaphore = self.prim_storage.get_sync_prim(
                key=self._key,
                value=self.value
            )

        # Check waiters before release for not deleting key too early
        waiters_before_release = bool(self._current_semaphore.waiters)

        # In case when Semaphore released more times than acquired
        if self.value <= self._current_semaphore.value:
            self._current_semaphore.init_value = self.value = self._current_semaphore.value + 1

        self._current_semaphore.semaphore.release()
        if from_context_manager:
            self._current_semaphore.pending -= 1

        # Todo remove unnecessary checks if there is, need investigation
        if (not self._current_semaphore.semaphore.locked() and
                not self._current_semaphore.waiters and
                not waiters_before_release and
                self._current_semaphore.value == self.value and
                self._current_semaphore.pending == 0):
            self.prim_storage.del_sync_prim(self._key)

    def locked(self) -> bool:
        return self.prim_storage.locked(self._key)

    def resolve_storage(self, storage_data: StorageData[Semaphore]) -> SemaphoreStorage:
        return SemaphoreStorage(storage_data=storage_data)
