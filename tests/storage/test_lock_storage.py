import pytest

from aiopriman.storage import LockStorage, StorageData


def test_lock_storage_with_storage_data():
    data = StorageData()
    storage = LockStorage(storage_data=data)
    assert not storage.locked("test")
    assert not data
    assert data is storage.sync_prims and isinstance(data, StorageData)


def test_lock_storage_without_storage_data():
    storage = LockStorage()
    assert isinstance(storage.sync_prims, StorageData)


@pytest.mark.asyncio
async def test_lock_storage_locked():
    data = StorageData()
    storage = LockStorage(storage_data=data)
    lock = storage.get_sync_prim(key="test")
    await lock.lock.acquire()
    assert storage.locked("test")
