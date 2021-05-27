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
    async with SemaphoreManager(storage_data=storage, key="test", value=2) as sem:
        logging.debug(f"HERE SEM LOCKED {name}: {sem}")
        await asyncio.sleep(3)


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s",
    )

    tasks = []
    storage_data = StorageData()
    for i in range(1, 10):
        tasks.append(run_lock(storage_data, i))
        tasks.append(run_sem(storage_data, i))

    asyncio.run(main_run(*tasks))
