from __future__ import annotations

from typing import Generic, TypeVar

from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseManager(ABC, Generic[T]):
    def __init__(self, prim_storage, key):
        self._prim_storage = prim_storage
        self._key = key

    @abstractmethod
    async def __aenter__(self) -> T: ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
