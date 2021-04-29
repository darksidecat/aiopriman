import pytest

from asyncio_lock_manager.storage import LockStorage


@pytest.fixture()
def lock_storage():
    return LockStorage("Test")
