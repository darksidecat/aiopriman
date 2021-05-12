"""
Manager factory that return required manager
"""
from __future__ import annotations

import inspect
from functools import partial
from typing import List, Optional, Type, TypeVar, Union, cast

from aiopriman.storage import BaseStorage, StorageData
from aiopriman.sync_primitives import SyncPrimitive

from .base_manager import BaseManager
from .lock_manager import LockManager
from .semaphore_manager import SemaphoreManager

T_co = TypeVar('T_co', bound=SyncPrimitive, covariant=True)
T_Storage = TypeVar('T_Storage', bound=BaseStorage[SyncPrimitive])


class Types:
    """
    Manager types
    """
    LOCK = LockManager
    SEM = SemaphoreManager

    @classmethod
    def props(cls) -> List[str]:
        members = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        return [attr[0] for attr in members if not str(attr[0]).startswith("_")]


class Manager:
    """
    Manager factory that return required manager

    Inputs:
        T_co : subclass of SyncPrimitive
        T_Storage : subclass of SyncPrimitiveStorage
    """

    def __init__(self,
                 types: Type[Types] = Types,
                 storage_data: Optional[StorageData[T_co]] = None):
        """
        :param types: manager types
        :param storage_data: StorageData
        """
        self.types = types
        self.storage_data = storage_data if storage_data else StorageData()

    def get(self,
            man_type: Union[
                Type[BaseManager[T_co, T_Storage]],
                str]) -> Type[BaseManager[T_co, T_Storage]]:
        """
        Get class based on man_type value with settled with functools.partial storage_date

        :param man_type: Manager type
        """
        if isinstance(man_type, str):
            if man_type in self.types.props():
                return cast(
                    Type[BaseManager[T_co, T_Storage]],
                    partial(getattr(self.types, man_type),
                            storage_data=self.storage_data))
            else:
                raise ValueError("This manager type is not specified in Types")
        elif inspect.isclass(man_type) and issubclass(man_type, BaseManager):
            return cast(
                Type[BaseManager[T_co, T_Storage]],
                partial(man_type, storage_data=self.storage_data))
        else:
            raise TypeError("man_type must be str or BaseManager subclass")
