"""
Condition synchronization primitive
"""
from __future__ import annotations

import asyncio
from typing import Any, Deque

from .sync_primitive import SyncPrimitive


class Condition(SyncPrimitive):
    """
    Condition synchronization primitive
    """

    def __init__(self, key: str):
        """
        :param key: key
        """
        super().__init__(key)
        self.condition: asyncio.Condition = asyncio.Condition()

    # noinspection PyProtectedMember
    @property
    def waiters(self) -> Deque[asyncio.Future[Any]]:
        """
        :return: waiters
        """
        return self.condition._waiters  # type: ignore

    def __repr__(self) -> str:
        return str(
            "Condition(key={key}, value={condition})".format(
                key=self.key,
                condition=self.condition
            )
        )

    def __str__(self) -> str:
        return self.__repr__()
