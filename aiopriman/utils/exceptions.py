"""
Exceptions
"""


class CantDeleteWithWaiters(Exception):
    """Sync primitive with waiters cant be deleted"""

    pass


class CantDeleteSemaphoreWithAcquire(Exception):
    """Semaphore with acquire cant be deleted"""

    pass
