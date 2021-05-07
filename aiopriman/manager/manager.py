"""
Manager factory that return required manager
"""
from __future__ import annotations

from enum import Enum
from functools import partial
from typing import Optional, Type, TypeVar, Union, cast

from ..storage import StorageData, SyncPrimitiveStorage
from ..sync_primitives import SyncPrimitive
from .base_manager import BaseManager
from .lock_manager import LockManager
from .semaphore_manager import SemaphoreManager

T_co = TypeVar('T_co', bound=SyncPrimitive, covariant=True)
T_Storage = TypeVar('T_Storage', bound=SyncPrimitiveStorage[SyncPrimitive])


class Types(Enum):
    """
    Manager types
    """
    LOCK = LockManager
    SEM = SemaphoreManager


class Manager:
    """
    Manager factory that return required manager

    Inputs:
        T_co : subclass of SyncPrimitive
        T_Storage : subclass of SyncPrimitiveStorage
    """

    def __init__(self, storage_data: Optional[StorageData[T_co]] = None):
        """
        :param storage_data: StorageData
        """
        self.storage_data = storage_data if storage_data else StorageData()

    def get(self, man_type: Union[Types, str]) -> Type[BaseManager[T_co, T_Storage]]:
        """
        Get class based on man_type value with settled with functools.partial storage_date

        :param man_type: Manager type
        """
        if isinstance(man_type, Types):
            return cast(
                Type[BaseManager[T_co, T_Storage]],
                partial(man_type.value, storage_data=self.storage_data))
        elif isinstance(man_type, str):
            return cast(
                Type[BaseManager[T_co, T_Storage]],
                partial(Types[man_type].value, storage_data=self.storage_data))
        else:
            raise TypeError("man_type must be str or manager.Types instance")
