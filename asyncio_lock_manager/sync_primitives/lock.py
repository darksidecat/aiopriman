"""
Lock synchronization primitive
"""
import asyncio
from dataclasses import dataclass, field
from typing import Optional, Deque


@dataclass
class Lock:
    key: str
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    # noinspection PyProtectedMember
    @property
    def waiters(self) -> Optional[Deque]:
        return self.lock._waiters  # type: ignore
