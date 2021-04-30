import asyncio

import pytest

from asyncio_lock_manager.manager import LockManager
from asyncio_lock_manager.utils.exceptions import CantDeleteWithWaiters


def test_lock_manager_without_context_empty():
    lock_manager = LockManager()
    assert not lock_manager.prim_storage.sync_prims


def test_lock_manager_without_context_add_lock():
    lock_manager = LockManager()
    lock_manager.prim_storage.get_sync_prim(key="test")
    assert lock_manager.prim_storage.sync_prims
    assert "Lock:test" in lock_manager.prim_storage.sync_prims


@pytest.mark.asyncio
async def test_lock_manager_with_context():
    lock_manager = LockManager(key="test")
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(lock_manager.prim_storage.sync_prims))
    async with lock_manager:
        assert "Lock:test" in lock_manager.prim_storage.sync_prims
        locks_acquire_result.append(bool(lock_manager.prim_storage.sync_prims))
    locks_acquire_result.append(bool(lock_manager.prim_storage.sync_prims))
    assert locks_acquire_result == expected


@pytest.mark.asyncio
async def test_lock_manager_raise_waiters_exc():
    async def task(lock_manager):
        async with lock_manager:
            await asyncio.sleep(0.2)

    async def task2(lock_manager):
        async with lock_manager:
            await asyncio.sleep(0.2)

    async def task_del(lock_manager):
        await asyncio.sleep(0.1)
        with pytest.raises(CantDeleteWithWaiters):
            lock_manager.prim_storage.del_sync_prim("test")

    lock_manager = LockManager(key="test")
    await asyncio.gather(task(lock_manager),
                         task2(lock_manager),
                         task_del(lock_manager))


@pytest.mark.asyncio
async def test_lock_manager_log_miss_key(caplog):
    lock_manager = LockManager()
    lock_manager.prim_storage.del_sync_prim("test")
    assert 'Can`t find lock by key to delete' in caplog.text
