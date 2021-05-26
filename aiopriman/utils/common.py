import inspect
from typing import Any, Dict


def inspect_params(obj: Any, **kwargs: Any) -> Dict[str, Any]:
    payload = {}
    params = inspect.signature(obj).parameters.keys()

    for k, v in kwargs.items():
        if k in params:
            payload[k] = v

    return payload
