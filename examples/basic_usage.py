import asyncio
import logging

import asyncio_lock_manager as alm


async def run(storage, name):
    logging.debug(f"START {name}")
    storage.get_sync_prim("1111")
    storage.get_sync_prim("2222")

    logging.debug(f"ENTER LOCKS {name}: {storage.sync_prims}")

    async with alm.manager.LockManager(storage, "test") as lock:
        logging.debug(f"HERE LOCKED {name}: {lock}")
        await asyncio.sleep(3)
        storage.del_sync_prim("1111")
        logging.debug(f"CONTEXT LOCKS {name}: {storage.sync_prims}")

    logging.debug(f"HERE UNLOCKED {name}: {lock}")
    logging.debug(f"EXIT LOCKS {name}: {storage.sync_prims}")


async def run2(storage, name):
    logging.debug(f"START {name}")
    logging.debug(f"ENTER LOCKS {name}: {storage.sync_prims}")

    lock = storage.get_sync_prim("1111")
    logging.debug(f"{name}: {lock}")
    try:
        await lock.sync_prims.acquire()
        await asyncio.sleep(3)
        logging.debug(f"CONTEXT LOCKS {name}: {storage.sync_prims}")
        logging.debug(f"{name}: {lock}")
        storage.del_sync_prim("1111")
    finally:
        logging.debug(f"{name}: {lock}")
        lock.sync_prims.release()
        logging.debug(f"{name}: {lock}")

    logging.debug(f"HERE UNLOCKED {name}: {lock}")
    logging.debug(f"EXIT LOCKS {name}: {storage.sync_prims}")


async def run3(storage, name):
    logging.debug(f"START {name}")
    logging.debug(f"ENTER SEM {name}: {storage.sync_prims}")

    lock = storage.get_sync_prim("****", value=3)
    logging.debug(f"{name}: {lock}")
    try:
        await lock.sync_prims.acquire()
        await lock.sync_prims.acquire()
        await asyncio.sleep(3)
        logging.debug(f"CONTEXT SEM {name}: {storage.sync_prims}")
        logging.debug(f"{name}: {lock}")
        storage.del_sync_prim("****")
    finally:
        logging.debug(f"{name}: {lock}")
        lock.sync_prims.release()
        logging.debug(f"{name}: {lock}")

    logging.debug(f"HERE UNLOCKED SEM {name}: {lock}")
    logging.debug(f"EXIT SEM {name}: {storage.sync_prims}")


async def main_run(*args):
    await asyncio.gather(*args)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:(%(filename)s).%(funcName)s(%(lineno)d):%(message)s'
    )
    lock_storage = alm.storage.LockStorage("base")
    semaphore_storage = alm.storage.SemaphoreStorage("sem")
    asyncio.run(
        main_run(
            run(lock_storage, "1"),
            run(lock_storage, "2"),
            run2(lock_storage, "A"),
            run2(lock_storage, "B"),
            run3(semaphore_storage, "-"),
            run3(semaphore_storage, "*"),
        )
    )
