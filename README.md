# asyncio_lock_manager

[![codecov](https://codecov.io/gh/darksidecat/aiopriman/branch/main/graph/badge.svg?token=Z0P6ZKJV43)](https://codecov.io/gh/darksidecat/aiopriman)


# Usage Examples

```python3
from __future__ import annotations

import asyncio
import logging
from typing import Type

from aiopriman.manager import Manager, Types, LockManager, SemaphoreManager


async def task_lock(manager):
    lock_man: Type[LockManager] = manager.get(Types.LOCK)

    logging.debug(manager.storage_data)
    async with lock_man(key='lock_key') as lock:
        logging.debug(f"HERE LOCKED: {lock}")
        await asyncio.sleep(3)
    logging.debug(manager.storage_data)


async def task_sem(manager):
    sem_man: Type[SemaphoreManager] = manager.get(Types.SEM)

    logging.debug(manager.storage_data)
    async with sem_man(key='sem_key', value=2) as sem:
        logging.debug(f"HERE SEM LOCK: {sem}")
        await asyncio.sleep(3)
    logging.debug(manager.storage_data)


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )

    manager = Manager()
    asyncio.run(
        main_run(
            task_lock(manager),
            task_lock(manager),
            task_lock(manager),
            task_lock(manager),
            task_sem(manager),
            task_sem(manager),
            task_sem(manager),
            task_sem(manager),
        )
    )

```