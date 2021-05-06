"""
Abstract asyncio synchronization primitive storage
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar, Optional

from aiopriman.sync_primitives import SyncPrimitive

T_co = TypeVar('T_co', bound=SyncPrimitive, covariant=True)


class StorageData(Dict[str, T_co]):
    """
    A class containing synchronization primitives
    """
    pass


class SyncPrimitiveStorage(ABC, Generic[T_co]):
    """
    Abstract asyncio synchronization primitives storage

    Inputs:
        T_co : subclass of SyncPrimitive
    """

    def __init__(self, storage_data: Optional[StorageData[T_co]] = None):
        """
        :param storage_data: StorageData
        """
        if storage_data is not None:
            self.sync_prims = storage_data
        else:
            self.sync_prims = StorageData()

    @abstractmethod
    def get_sync_prim(self, key: str) -> T_co:
        """
        Return synchronization primitive from storage,
        if key not exist in storage then create this primitive

        :param key: key
        :return: synchronization primitive
        """

    @abstractmethod
    def del_sync_prim(self, key: str) -> None:
        """
        Delete synchronization primitive from storage,
        if key can`t be deleted raise CantDeleteWithWaiters exception
        if key not found logging this

        :param key: key
        :return:
        """

    @staticmethod
    def resolve_key(prefix: str, key: str) -> str:
        """
        Resolve key for current storage type

        :param prefix: prefix
        :param key: key
        :return: "prefix:key"
        """
        return ":".join([prefix, key])

    @property
    def prefix(self) -> str:
        """
        Prefix for storage key resolving

        :return: prefix
        """
        return self.__class__.__name__
