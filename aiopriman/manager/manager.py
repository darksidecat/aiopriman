from enum import Enum
from functools import partial

from .lock_manager import LockManager
from .semaphore_manager import SemaphoreManager
from ..storage.base_storage import StorageData


class Types(Enum):
    LOCK = LockManager
    SEM = SemaphoreManager


class Manager:
    def __init__(self):
        self.storage_data = StorageData()

    def get(self, man_type):
        if isinstance(man_type, Types):
            return partial(man_type.value, storage_data=self.storage_data)
        elif isinstance(man_type, str):
            return partial(Types[man_type].value, storage_data=self.storage_data)
        else:
            raise TypeError("man_type must be str or manager.Types instance")
