import pytest

from aiopriman.storage import StorageData


@pytest.fixture
def storage_data():
    return StorageData()
