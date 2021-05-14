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

### Working with a specific type of Manager, storage data must be specified as a parameter
```python3
import asyncio
import logging

from aiopriman.manager import LockManager, SemaphoreManager
from aiopriman.storage import StorageData


async def run_lock(storage, name):
    logging.debug(f"START Lock {name}")
    async with LockManager(storage_data=storage, key="test") as lock:
        logging.debug(f"HERE LOCKED {name}: {lock}")
        await asyncio.sleep(3)


async def run_sem(storage, name):
    logging.debug(f"START Sem {name}")
    async with SemaphoreManager(storage_data=storage,  key="test", value=2) as sem:
        logging.debug(f"HERE SEM LOCKED {name}: {sem}")
        await asyncio.sleep(3)


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )

    tasks = []
    storage_data = StorageData()
    for i in range(1, 10):
        tasks.append(run_lock(storage_data, i))
        tasks.append(run_sem(storage_data, i))

    asyncio.run(
        main_run(
           *tasks
        )
    )


```