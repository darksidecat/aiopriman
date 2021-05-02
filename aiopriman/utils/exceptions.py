"""
Exceptions
"""


class CantDeleteWithWaiters(Exception):
    """Sync primitive with waiters cant be deleted"""
    pass


class CantDeleteSemaphoreWithMoreThanOneAcquire(Exception):
    """Semaphore with more than one current acquire cant be deleted"""
    pass
