"""
Abstract asyncio synchronization primitive
"""
from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

T = TypeVar('T')


class SyncPrimitive(ABC, Generic[T]):
    """
    Abstract asyncio synchronization primitive
    """

    def __init__(self, key: str):
        """
        :param key: key
        :type key: str
        """
        self.key = key
