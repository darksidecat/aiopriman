import pytest

from asyncio_lock_manager.manager import LockManager


def test_lock_manager_without_context(lock_storage):
    LockManager(lock_storage, key="test_key")
    assert not lock_storage.locks


@pytest.mark.asyncio
async def test_lock_manager_with_context(lock_storage):
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(lock_storage.locks))
    async with LockManager(lock_storage, key="test_key"):
        locks_acquire_result.append(bool(lock_storage.locks))
    locks_acquire_result.append(bool(lock_storage.locks))
    assert locks_acquire_result == expected
