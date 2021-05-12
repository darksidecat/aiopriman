from abc import abstractmethod
from types import TracebackType
from typing import Optional, Type

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
