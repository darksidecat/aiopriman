from aiopriman.utils.common import inspect_params


def test_inspect_params():
    def func(a, b):
        pass
    kwargs = {'a': 1, 'b': 2, 'c': 3}
    assert inspect_params(func, **kwargs) == {'a': 1, 'b': 2}
