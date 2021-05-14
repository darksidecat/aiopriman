import asyncio

import pytest

from aiopriman.manager import SemaphoreManager
from aiopriman.sync_primitives import Semaphore
from aiopriman.utils.exceptions import (CantDeleteSemaphoreWithAcquire,
                                        CantDeleteWithWaiters)


def test_sem_manager_without_context_empty(storage_data):
    sem_manager = SemaphoreManager(storage_data)
    assert not sem_manager.prim_storage.sync_prims


def test_sem_manager_without_context_add_lock(storage_data):
    sem_manager = SemaphoreManager(storage_data)
    sem_manager.prim_storage.get_sync_prim(key="test")
    assert sem_manager.prim_storage.sync_prims
    assert "SemaphoreStorage:test" in sem_manager.prim_storage.sync_prims


@pytest.mark.asyncio
async def test_sem_manager_with_context(storage_data):
    sem_manager = SemaphoreManager(storage_data, key="test")
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(sem_manager.prim_storage.sync_prims))
    async with sem_manager:
        assert "SemaphoreStorage:test" in sem_manager.prim_storage.sync_prims
        locks_acquire_result.append(bool(sem_manager.prim_storage.sync_prims))
    locks_acquire_result.append(bool(sem_manager.prim_storage.sync_prims))
    assert locks_acquire_result == expected


@pytest.mark.asyncio
async def test_sem_manager_raise_waiters_exc(storage_data):
    async def task(sem_manager):
        async with sem_manager:
            await asyncio.sleep(0.2)

    async def task2(sem_manager):
        async with sem_manager:
            await asyncio.sleep(0.2)

    async def task_del(sem_manager):
        await asyncio.sleep(0.1)
        with pytest.raises(CantDeleteWithWaiters):
            sem_manager.prim_storage.del_sync_prim("test")

    sem_manager = SemaphoreManager(storage_data, key="test")
    await asyncio.gather(task(sem_manager),
                         task2(sem_manager),
                         task_del(sem_manager))


@pytest.mark.asyncio
async def test_sem_manager_raise_more_than_one_aquire(storage_data):
    async def task(sem_manager):
        async with sem_manager:
            await asyncio.sleep(0.2)

    async def task2(sem_manager):
        async with sem_manager:
            await asyncio.sleep(0.2)

    async def task_del(sem_manager):
        await asyncio.sleep(0.1)
        with pytest.raises(CantDeleteSemaphoreWithAcquire):
            sem_manager.prim_storage.del_sync_prim("test")

    sem_manager = SemaphoreManager(storage_data, key="test", value=2)
    await asyncio.gather(task(sem_manager),
                         task2(sem_manager),
                         task_del(sem_manager))


def test_sem_manager_log_miss_key(caplog, storage_data):
    sem_manager = SemaphoreManager(storage_data)
    sem_manager.prim_storage.del_sync_prim("test")
    assert 'Can`t find semaphore by key to delete' in caplog.text


@pytest.mark.asyncio
async def test_sem_increasing_value(storage_data):
    init_value = 2
    sem_manager = SemaphoreManager(storage_data, key="test", value=init_value)
    async with sem_manager:
        sem: Semaphore = sem_manager.prim_storage.get_sync_prim(key="test")
        sem.semaphore.release()
    assert [sem.init_value, sem.value, sem_manager.value] == [init_value+1]*3
    assert not sem_manager.prim_storage.sync_prims


@pytest.mark.asyncio
async def test_sem_increasing_value_more_than_one(storage_data):
    init_value = 2
    sem_manager = SemaphoreManager(storage_data, key="test", value=init_value)
    async with sem_manager:
        sem: Semaphore = sem_manager.prim_storage.get_sync_prim(key="test")
        sem.semaphore.release()
        sem.semaphore.release()
    assert [sem.init_value, sem.value, sem_manager.value] == [init_value+2]*3
    assert not sem_manager.prim_storage.sync_prims


@pytest.mark.asyncio
async def test_sem_no_cant_find_key_warning_odd(caplog, storage_data):
    async def task(sem_manager):
        async with sem_manager:
            await asyncio.sleep(0.2)

    sem_manager = SemaphoreManager(storage_data, key="test", value=2)
    await asyncio.gather(task(sem_manager),
                         task(sem_manager),
                         task(sem_manager),
                         )
    assert 'Can`t find semaphore by key to delete' not in caplog.text


@pytest.mark.asyncio
async def test_sem_no_cant_find_key_warning_even(caplog, storage_data):
    async def task(sem_manager):
        async with sem_manager:
            await asyncio.sleep(0.2)

    sem_manager = SemaphoreManager(storage_data, key="test", value=2)
    await asyncio.gather(task(sem_manager),
                         task(sem_manager),
                         task(sem_manager),
                         task(sem_manager),
                         )
    assert 'Can`t find semaphore by key to delete' not in caplog.text


@pytest.mark.asyncio
async def test_sem_release_deleting(storage_data):
    init_value = 2
    sem_manager = SemaphoreManager(storage_data, key="test", value=init_value)
    sem_manager.release()
    assert not sem_manager.prim_storage.sync_prims
