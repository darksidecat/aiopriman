import inspect
from typing import Any, Dict, Optional, List


def inspect_params(obj: Any, skip: Optional[List[str]] = None, **kwargs: Any) -> Dict[str, Any]:
    if skip is None:
        skip = []

    payload = {}
    params = inspect.signature(obj).parameters.keys()

    for k, v in kwargs.items():
        if k in params and k not in skip:
            payload[k] = v

    return payload
