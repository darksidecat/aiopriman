import asyncio
import logging
from typing import Type

import aiopriman
from aiopriman.manager import Manager, LockManager, SemaphoreManager


async def run_lock(manager, name):
    man: Type[LockManager] = manager.get(aiopriman.manager.Types.LOCK)

    logging.debug(f"START {name}")
    async with man(key="test") as lock:
        logging.debug(f"HERE LOCKED {name}: {lock}")
        await asyncio.sleep(3)


async def run_sem(manager, name):
    man: Type[SemaphoreManager] = manager.get(aiopriman.manager.Types.SEM)

    logging.debug(f"START {name}")
    async with man(key="test", value=2) as lock:
        logging.debug(f"HERE SEM LOCKED {name}: {lock}")
        await asyncio.sleep(3)


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )

    tasks = []
    manager = Manager()
    for i in range(1, 10):
        tasks.append(run_lock(manager, i))
        tasks.append(run_sem(manager, i))

    asyncio.run(
        main_run(
           *tasks
        )
    )
