"""
Lock storage
"""
from __future__ import annotations

import logging
from typing import Dict

from asyncio_lock_manager.sync_primitives.lock import Lock


class LockStorage:
    def __init__(self, name: str):
        self.name: str = name
        self.locks: Dict[str, Lock] = dict()

    def get_lock(self, key: str) -> Lock:
        return self.locks.setdefault(key, Lock(key))

    def del_lock(self, key: str) -> None:
        lock = self.locks.get(key)
        if lock and lock.waiters:
            logging.warning("Can`t delete lock with waiters %s" % lock)
            return
        try:
            del self.locks[key]
        except KeyError as err:
            logging.warning("Can`t find lock by key to delete %s" % err)
