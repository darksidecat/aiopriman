from functools import wraps

from aiopriman.utils.common import _check_spec, _get_spec, inspect_params


def test_inspect_params():
    def func(a, b):
        pass

    kwargs = {"a": 1, "b": 2, "c": 3}
    assert inspect_params(func, **kwargs) == {"a": 1, "b": 2}


def test_get_spec_wrapped():
    def dummy_decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            func(*args, **kwargs)

        return wrapped

    @dummy_decorator
    def func(a, b):
        pass

    def func2(a, b):
        pass

    assert _get_spec(func) == _get_spec(func2)


def test_check_spec():
    kwargs = {"a": 1, "b": 2, "c": 3}

    def func(a, b, **kwargs):
        pass

    assert _check_spec(_get_spec(func), kwargs) == kwargs

