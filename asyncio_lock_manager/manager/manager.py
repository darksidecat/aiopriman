from enum import Enum
from typing import Union, Callable

from .lock_manager import LockManager
from .semaphore_manager import SemaphoreManager


class Types(Enum):
    LOCK = LockManager
    SEM = SemaphoreManager


class Manager:
    def __init__(self, man_type: Union[Types, str], lock_storage, key):
        type_ = man_type.value if isinstance(man_type, Types) else Types[man_type].value
        self.cls: Callable = type_
        self.inst = self.cls(lock_storage, key)

    async def __aenter__(self):
        await self.inst.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.inst.__aexit__(exc_type, exc_val, exc_tb)
