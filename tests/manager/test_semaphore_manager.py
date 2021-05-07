import asyncio

import pytest

from aiopriman.manager import SemaphoreManager
from aiopriman.sync_primitives import Semaphore
from aiopriman.utils.exceptions import CantDeleteWithWaiters, \
    CantDeleteSemaphoreWithAcquire


def test_sem_manager_without_context_empty():
    sem_manager = SemaphoreManager()
    assert not sem_manager.prim_storage.sync_prims


def test_sem_manager_without_context_add_lock():
    sem_manager = SemaphoreManager()
    sem_manager.prim_storage.get_sync_prim(key="test")
    assert sem_manager.prim_storage.sync_prims
    assert "SemaphoreStorage:test" in sem_manager.prim_storage.sync_prims


@pytest.mark.asyncio
async def test_sem_manager_with_context():
    sem_manager = SemaphoreManager(key="test")
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(sem_manager.prim_storage.sync_prims))
    async with sem_manager:
        assert "SemaphoreStorage:test" in sem_manager.prim_storage.sync_prims
        locks_acquire_result.append(bool(sem_manager.prim_storage.sync_prims))
    locks_acquire_result.append(bool(sem_manager.prim_storage.sync_prims))
    assert locks_acquire_result == expected


@pytest.mark.asyncio
async def test_sem_manager_raise_waiters_exc():
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

    sem_manager = SemaphoreManager(key="test")
    await asyncio.gather(task(sem_manager),
                         task2(sem_manager),
                         task_del(sem_manager))


@pytest.mark.asyncio
async def test_sem_manager_raise_more_than_one_aquire():
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

    sem_manager = SemaphoreManager(key="test", value=2)
    await asyncio.gather(task(sem_manager),
                         task2(sem_manager),
                         task_del(sem_manager))


@pytest.mark.asyncio
async def test_sem_manager_log_miss_key(caplog):
    sem_manager = SemaphoreManager()
    sem_manager.prim_storage.del_sync_prim("test")
    assert 'Can`t find semaphore by key to delete' in caplog.text


@pytest.mark.asyncio
async def test_sem_increasing_value():
    init_value = 2
    sem_manager = SemaphoreManager(key="test", value=init_value)
    async with sem_manager:
        sem: Semaphore = sem_manager.prim_storage.get_sync_prim(key="test")
        sem.semaphore.release()
    assert [sem.init_value, sem.value, sem_manager.value] == [init_value+1]*3
    assert not sem_manager.prim_storage.sync_prims
