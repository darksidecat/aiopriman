import pytest

from aiopriman.manager import LockManager
from aiopriman.manager.utils import lock
from aiopriman.storage import StorageData


@pytest.mark.asyncio
async def test_lock_raise_need_keyword():
    @lock(LockManager)
    async def func():
        pass

    with pytest.raises(ValueError):
        await func()


@pytest.mark.asyncio
async def test_lock(storage_data):
    @lock(LockManager)
    async def func():
        assert "LockStorage:test" in storage_data
        assert storage_data["LockStorage:test"].lock.locked()

    await func(storage_data=storage_data, key="test")


@pytest.mark.asyncio
async def test_lock_func_params(storage_data):
    storage_data_func = storage_data
    storage_data_dec = StorageData()

    @lock(LockManager, storage_data=storage_data_dec, key="test2")
    async def func(storage_data):
        assert "LockStorage:test" in storage_data
        assert storage_data is storage_data_func

    await func(storage_data=storage_data, key="test")


@pytest.mark.asyncio
async def test_lock_dec_params(storage_data):
    storage_data_dec = StorageData()

    @lock(LockManager, storage_data=storage_data_dec, key="test2")
    async def func():
        assert "LockStorage:test2" in storage_data_dec

    await func()
