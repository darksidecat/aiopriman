"""
Abstract asyncio synchronization primitives manager
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from aiopriman.storage import BaseStorage, StorageData
from aiopriman.sync_primitives import SyncPrimitive

T_co = TypeVar('T_co', bound=SyncPrimitive, covariant=True)
T_Storage = TypeVar('T_Storage', bound=BaseStorage[SyncPrimitive])


class BaseManager(ABC, Generic[T_co, T_Storage]):
    """
    Abstract asyncio synchronization primitives manager

    Inputs:
        T_co : subclass of SyncPrimitive
        T_Storage : subclass of SyncPrimitiveStorage
    """

    def __init__(self, storage_data: StorageData[T_co],  key: str = "Default"):
        """
        :param key: Key for managing sync primitive
        :param storage_data: StorageData
        """
        self.storage_data = storage_data
        self.prim_storage: T_Storage = self.resolve_storage(self.storage_data)
        self._key = key

    @abstractmethod
    def resolve_storage(self, storage_data: StorageData[T_co]) -> T_Storage:
        """Resolve storage for current manager type

        This method must be overridden.

        :param storage_data: StorageData
        :return: Storage
        """
