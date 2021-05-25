import asyncio
import logging

from aiopriman.manager.lock_manager import lock
from aiopriman.manager.semaphore_manager import semaphore_lock
from aiopriman.storage import StorageData


@lock
async def run_lock(name, storage_data, **kwargs):
    logging.debug(f"HERE LOCKED {name}")
    await asyncio.sleep(3)


@semaphore_lock
async def run_sem(name,storage_data, **kwargs):
    logging.debug(f"HERE SEM LOCKED {name}")
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
        tasks.append(run_lock(i, storage_data=storage_data,  key="test"))
        tasks.append(run_sem(i, storage_data=storage_data, key="test", value=2))

    asyncio.run(
        main_run(
           *tasks
        )
    )
