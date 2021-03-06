import asyncio

import pytest

from aiopriman.manager import LockManager
from aiopriman.utils.exceptions import CantDeleteWithWaiters


def test_lock_manager_without_context_empty(storage_data):
    lock_manager = LockManager(storage_data)
    assert not lock_manager.prim_storage.sync_prims


def test_lock_manager_without_context_add_lock(storage_data):
    lock_manager = LockManager(storage_data)
    lock_manager.prim_storage.get_sync_prim(key="test")
    assert lock_manager.prim_storage.sync_prims
    assert "LockStorage:test" in lock_manager.prim_storage.sync_prims


@pytest.mark.asyncio
async def test_lock_manager_with_context(storage_data):
    lock_manager = LockManager(storage_data, key="test")
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(lock_manager.prim_storage.sync_prims))
    async with lock_manager:
        assert "LockStorage:test" in lock_manager.prim_storage.sync_prims
        locks_acquire_result.append(bool(lock_manager.prim_storage.sync_prims))
    locks_acquire_result.append(bool(lock_manager.prim_storage.sync_prims))
    assert locks_acquire_result == expected


@pytest.mark.asyncio
async def test_lock_manager_raise_waiters_exc(storage_data):
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

    lock_manager = LockManager(storage_data, key="test")
    await asyncio.gather(
        task(lock_manager), task2(lock_manager), task_del(lock_manager)
    )


@pytest.mark.asyncio
async def test_lock_manager_log_miss_key(caplog, storage_data):
    lock_manager = LockManager(storage_data)
    lock_manager.prim_storage.del_sync_prim("test")
    assert "Can`t find Lock by key to delete" in caplog.text


@pytest.mark.asyncio
async def test_lock_manager_release_first(storage_data):
    lock_manager = LockManager(storage_data, key="test")
    with pytest.raises(RuntimeError):
        lock_manager.release()

    assert not lock_manager.storage_data


@pytest.mark.asyncio
async def test_lock_manager_locked(storage_data):
    lock_manager = LockManager(storage_data, key="test")
    assert not lock_manager.locked()
    async with lock_manager:
        assert lock_manager.locked()
    assert not lock_manager.locked()
