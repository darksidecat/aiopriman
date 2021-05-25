import inspect
from abc import abstractmethod
from functools import wraps
from types import TracebackType
from typing import Optional, Type, Any, Dict

from aiopriman.sync_primitives import SyncPrimitive


class _ContextManagerMixin:
    async def __aenter__(self) -> SyncPrimitive:
        return await self.acquire(from_context_manager=True)

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        self.release(from_context_manager=True)

    @abstractmethod
    async def acquire(self, from_context_manager: bool) -> SyncPrimitive:
        """Acquire synchronization primitive"""

    @abstractmethod
    def release(self, from_context_manager: bool) -> None:
        """Release synchronization primitive"""


def inspect_params(obj: Any, **kwargs: Any) -> Dict[str, Any]:
    payload = {}
    man_params = inspect.signature(obj).parameters.keys()

    for k, v in kwargs.items():
        if k in man_params:
            payload[k] = v

    return payload


def lock(manager, storage_data=None, **dec_kwargs):
    def decorator(func):

        @wraps(func)
        async def wrapped(*args, **kwargs):
            func_storage_data = kwargs.get('storage_data')
            storage_data_ = func_storage_data if func_storage_data is not None else storage_data
            if storage_data_ is None:
                raise ValueError("decorated function need keyword storage_data param")

            kwargs = {**dec_kwargs, **kwargs, "storage_data": storage_data_}
            man_params = inspect_params(manager, **kwargs)
            func_params = inspect_params(func, **kwargs)

            async with manager(**man_params):
                return await func(*args, **func_params)

        return wrapped
    return decorator
