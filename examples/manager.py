import asyncio
import logging

import asyncio_lock_manager as alm
from asyncio_lock_manager.manager import LockManager, SemaphoreManager


async def run(manager, name):
    man: [LockManager] = manager.get(alm.manager.Types.LOCK)

    logging.debug(f"START {name}")
    async with man(key="test") as lock:
        logging.debug(f"HERE LOCKED {name}: {lock}")
        await asyncio.sleep(3)


async def run2(manager, name):
    man: [SemaphoreManager] = manager.get(alm.manager.Types.SEM)

    logging.debug(f"START {name}")
    async with man(key="test2", storage_data=manager.storage_data) as lock:
        logging.debug(f"HERE SEM LOCKED {name}: {lock}")
        await asyncio.sleep(3)


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )

    manager = alm.manager.Manager()

    asyncio.run(
        main_run(
            run(manager, "1"),
            run(manager, "2"),
            run2(manager, "3"),
            run2(manager, "4"),
            run(manager, "1"),
            run(manager, "2"),
            run2(manager, "3"),
            run2(manager, "4"),
        )
    )
