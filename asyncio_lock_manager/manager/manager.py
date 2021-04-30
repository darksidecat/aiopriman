from enum import Enum
from typing import Union, Callable

from .lock_manager import LockManager
from .semaphore_manager import SemaphoreManager


class Types(Enum):
    LOCK = LockManager
    SEM = SemaphoreManager


class Manager:
    def __init__(self, man_type: Union[Types, str], lock_storage, key):
        self.man_type = man_type
        self.lock_storage = lock_storage
        self.key = key
        self.cls = None
        self.inst = None
        self.set_manager()

    def set_manager(self):
        if isinstance(self.man_type, Types):
            type_ = self.man_type.value
        else:
            type_ = Types[self.man_type].value
        self.cls: Callable = type_
        self.inst = self.cls(self.lock_storage, self.key)

    async def __aenter__(self):
        await self.inst.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.inst.__aexit__(exc_type, exc_val, exc_tb)
