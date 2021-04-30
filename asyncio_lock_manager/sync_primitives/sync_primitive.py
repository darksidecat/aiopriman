from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')


class SyncPrimitive(ABC, Generic[T]):
    def __init__(self, key: str):
        self.key = key
