"""
Abstract asyncio synchronization primitives manager
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from ..storage.base_storage import StorageData, SyncPrimitiveStorage
from ..sync_primitives import SyncPrimitive

T = TypeVar('T', bound=SyncPrimitive)
T_Storage = TypeVar('T_Storage', bound=SyncPrimitiveStorage)


class BaseManager(ABC, Generic[T, T_Storage]):
    """
    Abstract asyncio synchronization primitives manager

    Inputs:
        T : subclass of SyncPrimitive
        T_Storage : subclass of SyncPrimitiveStorage
    """

    def __init__(self, key=None, storage_data=None):
        """
        :param key: Key for managing sync primitive
        :type key: str
        :param storage_data: StorageData
        :type storage_data: StorageData, optional
        """
        self.storage_data = storage_data if storage_data is not None else StorageData()
        self.prim_storage: T_Storage = self.resolve_storage(self.storage_data)
        self._key = key

    @abstractmethod
    async def __aenter__(self) -> T: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    @abstractmethod
    def resolve_storage(self, storage_data) -> T_Storage:
        """Resolve storage for current manager type

        This method must be overridden.

        :param storage_data: StorageData
        :return: Storage
        :rtype: T_Storage
        """
