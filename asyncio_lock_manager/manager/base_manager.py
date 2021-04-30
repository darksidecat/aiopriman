from __future__ import annotations

from typing import Generic, TypeVar

from abc import ABC, abstractmethod

T = TypeVar('T')


class BaseManager(ABC, Generic[T]):
    def __init__(self, lock_storage, key):
        self._lock_storage = lock_storage
        self._key = key

    @abstractmethod
    async def __aenter__(self) -> T: ...

    @abstractmethod
    async def __aexit__(self, exc_type, value, traceback) -> None: ...
