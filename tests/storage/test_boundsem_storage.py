import pytest

from aiopriman.storage import BoundSemaphoreStorage, StorageData


def test_boundsem_storage_with_storage_data():
    data = StorageData()
    storage = BoundSemaphoreStorage(storage_data=data)
    assert not storage.locked("test")
    assert not data
    assert data is storage.sync_prims and isinstance(data, StorageData)


def test_sem_storage_without_storage_data():
    storage = BoundSemaphoreStorage()
    assert isinstance(storage.sync_prims, StorageData)


@pytest.mark.asyncio
async def test_sem_storage_locked():
    data = StorageData()
    storage = BoundSemaphoreStorage(storage_data=data)
    sem = storage.get_sync_prim(key="test")
    await sem.semaphore.acquire()
    assert storage.locked("test")
