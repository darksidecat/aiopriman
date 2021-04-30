from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar

T = TypeVar('T')


class SyncPrimitiveStorage(ABC, Generic[T]):
    def __init__(self, name: str):
        self.name: str = name
        self.sync_prims: Dict[str, T] = dict()

    @abstractmethod
    def get_sync_prim(self, key: str) -> T: ...

    @abstractmethod
    def del_sync_prim(self, key: str) -> None: ...
