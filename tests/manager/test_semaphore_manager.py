import pytest

from asyncio_lock_manager.manager import SemaphoreManager


def test_sem_manager_without_context(sem_storage):
    SemaphoreManager(sem_storage, key="test_key")
    assert not sem_storage.sync_prims


@pytest.mark.asyncio
async def test_sem_manager_with_context(sem_storage):
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(sem_storage.sync_prims))
    async with SemaphoreManager(sem_storage, key="test_key"):
        locks_acquire_result.append(bool(sem_storage.sync_prims))
    locks_acquire_result.append(bool(sem_storage.sync_prims))
    assert locks_acquire_result == expected
