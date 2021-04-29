"""
Lock synchronization primitive
"""
import asyncio
from dataclasses import dataclass, field


@dataclass
class Lock:
    key: str
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    # noinspection PyProtectedMember
    @property
    def waiters(self):
        return self.lock._waiters
