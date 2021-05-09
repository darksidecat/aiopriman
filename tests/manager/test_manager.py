import pytest

from aiopriman.manager import BaseManager, LockManager, Manager, Types


@pytest.mark.parametrize('prim_type', [
    1,
    1.5,
    {'a': "b"},
    [1, 2, 3],
])
def test_manager_invalid_prim_type(prim_type):
    m = Manager()
    with pytest.raises(TypeError):
        m.get(man_type=prim_type)


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


def test_manager_incorrect_type():
    m = Manager()
    with pytest.raises(ValueError):
        m.get(man_type="IncorrectTypeName")


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


def test_manager_custom_class():
    class T(Types):
        NEW = LockManager

    T.NEW2 = LockManager

    m = Manager(types=T)
    a = m.get(man_type="NEW")
    b = m.get(man_type=T.NEW)
    c = m.get(man_type="NEW2")

    assert a.func is b.func
    assert a.func is LockManager
    assert a.func is c.func
