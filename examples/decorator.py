import asyncio
import logging

from aiopriman.manager import LockManager, SemaphoreManager
from aiopriman.manager.utils import lock
from aiopriman.storage import StorageData

storage_data = StorageData()


@lock(LockManager, key="test2")  # will be used key value from function call
async def run_lock(name):
    logging.debug(f"HERE LOCKED {name}")
    await asyncio.sleep(3)


@lock(SemaphoreManager, storage_data=storage_data, key="test", value=5)  # using decorator params
async def run_sem(name):
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
        tasks.append(run_sem(i))

    asyncio.run(
        main_run(
           *tasks
        )
    )
