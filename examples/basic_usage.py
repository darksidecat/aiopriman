import asyncio
import logging

import asyncio_lock_manager as alm


async def run(storage, name):
    logging.debug(f"START {name}")
    storage.get_lock("1111")
    storage.get_lock("2222")

    logging.debug(f"ENTER LOCKS {name}: {storage.locks}")

    async with alm.manager.LockManager(storage, "test") as lock:
        logging.debug(f"HERE LOCKED {name}: {lock}")
        await asyncio.sleep(3)
        storage.del_lock("1111")
        logging.debug(f"CONTEXT LOCKS {name}: {storage.locks}")

    logging.debug(f"HERE UNLOCKED {name}: {lock}")
    logging.debug(f"EXIT LOCKS {name}: {storage.locks}")


async def run2(storage, name):
    logging.debug(f"START {name}")
    logging.debug(f"ENTER LOCKS {name}: {storage.locks}")

    lock = storage.get_lock("1111")
    logging.debug(f"{name}: {lock}")
    try:
        await lock.lock.acquire()
        await asyncio.sleep(3)
        logging.debug(f"CONTEXT LOCKS {name}: {storage.locks}")
        logging.debug(f"{name}: {lock}")
        storage.del_lock("1111")
    finally:
        logging.debug(f"{name}: {lock}")
        lock.lock.release()
        logging.debug(f"{name}: {lock}")

    logging.debug(f"HERE UNLOCKED {name}: {lock}")
    logging.debug(f"EXIT LOCKS {name}: {storage.locks}")


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )
    lock_storage = alm.storage.LockStorage("base")
    asyncio.run(
        main_run(
            run(lock_storage, "1"),
            run2(lock_storage, "A"),
            run(lock_storage, "2"),
            run2(lock_storage, "B"),
            run(lock_storage, "3"),
        )
    )
