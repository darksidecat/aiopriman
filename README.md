# Aiopriman

[![codecov](https://codecov.io/gh/darksidecat/aiopriman/branch/main/graph/badge.svg?token=Z0P6ZKJV43)](https://codecov.io/gh/darksidecat/aiopriman)
[![PyPi Package Version](https://img.shields.io/pypi/v/aiopriman?style=flat-square)](https://pypi.python.org/pypi/aiopriman)
[![PyPi status](https://img.shields.io/pypi/status/aiopriman?style=flat-square)](https://pypi.python.org/pypi/aiopriman)
[![Supported python versions](https://img.shields.io/pypi/pyversions/aiopriman?style=flat-square)](https://pypi.python.org/pypi/aiopriman)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/aiopriman?style=flat-square)](https://pypi.python.org/pypi/aiopriman)
[![MIT License](https://img.shields.io/pypi/l/aiopriman?style=flat-square)](https://opensource.org/licenses/MIT)

# Attention! the project is at the initial stage of development, so there may be changes that break backward compatibility

This package provides the ability to manage asyncio synchronization primitives.
Allows you to create storages of primitives, provides convenient means for accessing them using context managers,
factories, creation and access to synchronization primitives by key.

Designed to solve the problem of managing dynamically created synchronization primitives for different resources.

Primitives are stored in memory only when needed.

# Install
```pip install aiopriman```

# Usage Examples


### Work via Manager with shared storage data
```python3
import asyncio
import logging
from typing import Type

from aiopriman.manager import Manager, Types, LockManager, SemaphoreManager


async def task_lock(manager):
    lock_man: Type[LockManager] = manager.get(Types.LOCK)  # get LockManager with shared storage

    logging.debug(manager.storage_data)
    async with lock_man(key='lock_key') as lock:  # acquire lock for given key
        logging.debug(f"HERE LOCKED: {lock}")
        await asyncio.sleep(0.5)
    logging.debug(manager.storage_data)


async def task_sem(manager):
    sem_man: Type[SemaphoreManager] = manager.get(Types.SEM)  # get SemaphoreManager with shared storage

    logging.debug(manager.storage_data)
    async with sem_man(key='sem_key', value=2) as sem: # acquire semaphore lock for given key
        logging.debug(f"HERE SEM LOCK: {sem}")
        await asyncio.sleep(0.5)
    logging.debug(manager.storage_data)


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )

    tasks = []
    manager = Manager()  # initiate manager with shared storage
    for i in range(1, 10):
        tasks.append(task_lock(manager))
        tasks.append(task_sem(manager))

    asyncio.run(
        main_run(
           *tasks
        )
    )

```

### Working with a specific type of Manager, storage data must be specified as a parameter
```python3
import asyncio
from aiopriman.manager import LockManager, SemaphoreManager
from aiopriman.storage import StorageData


async def main():
    lock_man = LockManager(storage_data=storage_data, key="test")
    sem_man = SemaphoreManager(storage_data=storage_data, key="test", value=2)

    async with lock_man:
        async with sem_man:
            print(storage_data)
            #  {'LockStorage:test': Lock(key=LockStorage:test,
            #                       value=<asyncio.locks.Lock object at 0x000002D8F468E580 [locked]>),
            #  'SemaphoreStorage:test': Semaphore(key=SemaphoreStorage:test,
            #                           value=<asyncio.locks.Semaphore object at 0x000002D8F468E760
            #                           [unlocked, value:1]>, pending=1)}

    async with LockManager(key="test", storage_data=storage_data):
        #  or like this
        pass


if __name__ == '__main__':
    storage_data = StorageData()
    asyncio.run(main())


```