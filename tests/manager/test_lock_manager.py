import asyncio

import pytest

from asyncio_lock_manager.manager import LockManager
from asyncio_lock_manager.utils.exceptions import CantDeleteWithWaiters


def test_lock_manager_without_context(lock_storage):
    LockManager(lock_storage, key="test_key")
    assert not lock_storage.sync_prims


@pytest.mark.asyncio
async def test_lock_manager_with_context(lock_storage):
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(lock_storage.sync_prims))
    async with LockManager(lock_storage, key="test_key"):
        locks_acquire_result.append(bool(lock_storage.sync_prims))
    locks_acquire_result.append(bool(lock_storage.sync_prims))
    assert locks_acquire_result == expected


@pytest.mark.asyncio
async def test_lock_manager_raise_waiters_exc(sem_storage):
    async def task():
        async with LockManager(sem_storage, key="test_key"):
            await asyncio.sleep(0.2)

    async def task2():
        async with LockManager(sem_storage, key="test_key"):
            await asyncio.sleep(0.2)

    async def task_del():
        await asyncio.sleep(0.1)
        with pytest.raises(CantDeleteWithWaiters):
            sem_storage.del_sync_prim("test_key")

    await asyncio.gather(task(), task2(), task_del())
