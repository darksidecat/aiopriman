import pytest

from asyncio_lock_manager.manager import Manager, Types, BaseManager


@pytest.mark.parametrize('prim_type', [
    1,
    1.5,
    {'a': "b"},
    [1, 2, 3],
])
def test_manager_invalid_prim_type(prim_type):
    m = Manager()
    with pytest.raises(TypeError):
        m.get(man_type=prim_type)(key="test")


@pytest.mark.parametrize('prim_type', [
    Types.LOCK,
    Types.SEM,
    "LOCK",
    "SEM",
])
def test_manager_without_context_empty(prim_type):
    m = Manager()
    manager: [BaseManager] = m.get(man_type=prim_type)(key="test")
    assert not manager.prim_storage.sync_prims


@pytest.mark.parametrize('prim_type', [
    Types.LOCK,
    Types.SEM,
    "LOCK",
    "SEM",
])
@pytest.mark.asyncio
async def test_manager_with_context(prim_type):
    m = Manager()
    manager: [BaseManager] = m.get(man_type=prim_type)(key="test")
    locks_acquire_result = []
    expected = [False, True, False]

    locks_acquire_result.append(bool(manager.prim_storage.sync_prims))
    async with manager:
        locks_acquire_result.append(bool(manager.prim_storage.sync_prims))
    locks_acquire_result.append(bool(manager.prim_storage.sync_prims))
    assert locks_acquire_result == expected
