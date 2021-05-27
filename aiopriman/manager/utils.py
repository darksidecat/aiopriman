from abc import abstractmethod
from functools import wraps
from types import TracebackType
from typing import Any, AsyncContextManager, Callable, Optional, Type

from aiopriman.sync_primitives import SyncPrimitive
from aiopriman.utils.common import inspect_params


class _ContextManagerMixin:
    async def __aenter__(self) -> SyncPrimitive:
        return await self.acquire(from_context_manager=True)

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.release(from_context_manager=True)

    @abstractmethod
    async def acquire(self, from_context_manager: bool) -> SyncPrimitive:
        """Acquire synchronization primitive"""

    @abstractmethod
    def release(self, from_context_manager: bool) -> None:
        """Release synchronization primitive"""


def lock(
    manager: Callable[..., AsyncContextManager[Any]], **dec_kwargs: Any
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> Any:
            dec_storage_data = dec_kwargs.get("storage_data")
            func_storage_data = kwargs.get("storage_data")

            storage_data = (
                func_storage_data if func_storage_data is not None else dec_storage_data
            )
            if storage_data is None:
                raise ValueError("decorated function need keyword param storage_data")

            kwargs = {**dec_kwargs, **kwargs}

            man_params = inspect_params(manager, **kwargs)
            func_params = inspect_params(func, **kwargs)

            async with manager(**man_params):
                return await func(*args, **func_params)

        return wrapped

    return decorator
