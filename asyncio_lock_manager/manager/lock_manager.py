import asyncio


class LockManager:
    def __init__(self, lock_storage, key):
        self._lock_storage = lock_storage
        self._key = key

    async def __aenter__(self) -> asyncio.Lock:
        self._current_lock = self._lock_storage.get_lock(self._key)
        await self._current_lock.lock.acquire()
        return self._current_lock

    # noinspection PyProtectedMember
    async def __aexit__(self, exc_type, value, traceback):
        self._current_lock.lock.release()
        if not self._current_lock.lock._waiters:
            self._lock_storage.del_lock(self._key)
