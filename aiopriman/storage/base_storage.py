"""
Abstract asyncio synchronization primitive storage
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar

from aiopriman.sync_primitives import SyncPrimitive

T = TypeVar('T', bound=SyncPrimitive)


class StorageData(Dict):
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

    def __init__(self, storage_data=None):
        """
        :param storage_data: StorageData
        :type storage_data: StorageData, optional
        """
        self.sync_prims: Dict[str, T] = storage_data if storage_data is not None else StorageData()

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
    def resolve_key(prefix, key) -> str:
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
    def prefix(self):
        """
        Prefix for storage key resolving

        :return: prefix
        :rtype: str
        """
        return self.__class__.__name__
