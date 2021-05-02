"""
Exceptions
"""


class CantDeleteWithWaiters(Exception):
    """Sync primitive with waiters cant be deleted"""
    pass
