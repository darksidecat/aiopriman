"""
Abstract asyncio synchronization primitive storage
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar, Any, Optional

from aiopriman.sync_primitives import SyncPrimitive

T = TypeVar('T', bound=SyncPrimitive[Any])


class StorageData(Dict[str, T]):
    """
    A class containing synchronization primitives
    """
    pass


class SyncPrimitiveStorage(ABC, Generic[T]):
    """
    Abstract asyncio synchronization primitives storage

    Inputs:
        T : subclass of SyncPrimitive
    """

    def __init__(self, storage_data: Optional[StorageData[T]] = None):
        """
        :param storage_data: StorageData
        :type storage_data: StorageData, optional
        """
        if storage_data is not None:
            self.sync_prims = storage_data
        else:
            self.sync_prims = StorageData()

    @abstractmethod
    def get_sync_prim(self, key: str) -> T:
        """
        Return synchronization primitive from storage,
        if key not exist in storage then create this primitive

        :param key: key
        :type key: str
        :return: synchronization primitive
        :rtype: T
        """

    @abstractmethod
    def del_sync_prim(self, key: str) -> None:
        """
        Delete synchronization primitive from storage,
        if key can`t be deleted raise CantDeleteWithWaiters exception
        if key not found logging this

        :param key: key
        :type key: str
        :return:
        """

    @staticmethod
    def resolve_key(prefix: str, key: str) -> str:
        """
        Resolve key for current storage type

        :param prefix: prefix
        :type prefix: str
        :param key: key
        :type key: str
        :return: prefix:key
        :rtype: str
        """
        return ":".join([prefix, key])

    @property
    def prefix(self) -> str:
        """
        Prefix for storage key resolving

        :return: prefix
        :rtype: str
        """
        return self.__class__.__name__
