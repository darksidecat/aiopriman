"""
Abstract asyncio synchronization primitive
"""
from __future__ import annotations

from abc import ABC


class SyncPrimitive(ABC):
    """
    Abstract asyncio synchronization primitive
    """

    def __init__(self, key: str):
        """
        :param key: key
        :type key: str
        """
        self.key = key
