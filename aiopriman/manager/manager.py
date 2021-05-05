"""
Manager factory that return required manager
"""
from __future__ import annotations

from enum import Enum
from functools import partial
from typing import Type, cast, Optional, Union, TypeVar, Any, Generic

from . import BaseManager
from .lock_manager import LockManager
from .semaphore_manager import SemaphoreManager
from ..storage import StorageData, SyncPrimitiveStorage
from ..sync_primitives import SyncPrimitive

T = TypeVar('T', bound=SyncPrimitive[Any])
T_Storage = TypeVar('T_Storage', bound=SyncPrimitiveStorage[Any])


class Types(Enum):
    """
    Manager types
    """
    LOCK = LockManager
    SEM = SemaphoreManager


class Manager(Generic[T, T_Storage]):
    """
    Manager factory that return required manager

    Inputs:
        T : subclass of SyncPrimitive
        T_Storage : subclass of SyncPrimitiveStorage
    """

    def __init__(self, storage_data: Optional[StorageData[T]] = None):
        """
        :param storage_data: StorageData
        :type storage_data: StorageData
        """
        self.storage_data = storage_data if storage_data else StorageData()

    def get(self, man_type: Union[Types, str]) -> Type[BaseManager[T, T_Storage]]:
        """
        Get class based on man_type value with settled with functools.partial storage_date

        :param man_type: Manager type
        :type man_type: Types | str
        :return: Type[BaseManager]
        """
        if isinstance(man_type, Types):
            return cast(
                Type[BaseManager[T, T_Storage]],
                partial(man_type.value, storage_data=self.storage_data))
        elif isinstance(man_type, str):
            return cast(
                Type[BaseManager[T, T_Storage]],
                partial(Types[man_type].value, storage_data=self.storage_data))
        else:
            raise TypeError("man_type must be str or manager.Types instance")
