from __future__ import annotations

from typing import Generic, TypeVar

from abc import ABC, abstractmethod

from ..storage.base_storage import StorageData, SyncPrimitiveStorage


T = TypeVar('T')


class BaseManager(ABC, Generic[T]):
    def __init__(self, key=None, storage_data=None):
        self.storage_data = storage_data if storage_data is not None else StorageData()
        self.prim_storage: SyncPrimitiveStorage = self.resolve_storage(self.storage_data)
        self._key = key

    @abstractmethod
    async def __aenter__(self) -> T: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    def resolve_storage(self, storage_data): ...
