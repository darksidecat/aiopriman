from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar

T = TypeVar('T')


class StorageData(Dict):
    pass


class SyncPrimitiveStorage(ABC, Generic[T]):
    def __init__(self, storage_data=None):
        self.sync_prims: Dict[str, T] = storage_data if storage_data is not None else StorageData()

    @abstractmethod
    def get_sync_prim(self, key: str) -> T: ...

    @abstractmethod
    def del_sync_prim(self, key: str) -> None: ...

    @staticmethod
    def resolve_key(prefix, key):
        return "".join([prefix, key])
