import pytest

from asyncio_lock_manager.manager import Manager, Types


@pytest.mark.parametrize('prim_type', [
    Types.LOCK,
    Types.SEM,
    "LOCK",
    "SEM",
])
def test_manager_without_context(prim_type, prim_storage):
    Manager(prim_type, prim_storage, key="test_key")
    assert not prim_storage.sync_prims


@pytest.mark.parametrize('prim_type', [
    Types.LOCK,
    Types.SEM,
    "LOCK",
    "SEM",
])
@pytest.mark.asyncio
async def test_manager_with_context(prim_type, prim_storage):
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(prim_storage.sync_prims))
    async with Manager(prim_type, prim_storage, key="test_key"):
        locks_acquire_result.append(bool(prim_storage.sync_prims))
    locks_acquire_result.append(bool(prim_storage.sync_prims))
    assert locks_acquire_result == expected
