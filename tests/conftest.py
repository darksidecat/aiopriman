import pytest

from asyncio_lock_manager.storage import LockStorage, SemaphoreStorage


@pytest.fixture()
def prim_storage():
    # ToDO update after creating general storage
    return LockStorage("Test")


@pytest.fixture()
def lock_storage():
    return LockStorage("Test")


@pytest.fixture()
def sem_storage():
    return SemaphoreStorage("Test")
