import asyncio

from asyncio_lock_manager.sync_primitives.lock import Lock


class LockManager:
    def __init__(self, lock_storage, key):
        self._lock_storage = lock_storage
        self._key = key

    async def __aenter__(self) -> Lock:
        self._current_lock: Lock = self._lock_storage.get_lock(self._key)
        await self._current_lock.lock.acquire()
        return self._current_lock

    async def __aexit__(self, exc_type, value, traceback):
        self._current_lock.lock.release()
        if not self._current_lock.waiters:
            self._lock_storage.del_lock(self._key)
