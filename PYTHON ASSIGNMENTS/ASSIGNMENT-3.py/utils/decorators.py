import os
import asyncio
from functools import wraps
import inspect
# from core.devices import SmartCamera
from core.exceptions import PermissionDeniedError


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

log_path = os.path.join(BASE_DIR, "..", "manager", "logs.txt")
log_path = os.path.abspath(log_path)

def log_device_state_change(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            with open(log_path, "a+") as log:
                log.write(self.get_status_report() + "\n")
            return result
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            with open(log_path, "a+") as log:
                log.write(self.get_status_report() + "\n")
            return result
        return sync_wrapper
ACL = {
    "admin": {"*"},
    "user": {
        "turn_on",
        "turn_off",
        "set_volume",
        "play",
        "stop",
        "shift_track",
        "shuffle",
        "lock",
        "unlock",
    },
}


def role_guard(fn):
    @wraps(fn)
    async def wrapper(self, user_role: str, device_id: str, action_type: str, value=None):
        allowed = ACL.get(user_role.lower(), set())
        if action_type not in allowed and "*" not in allowed:
            raise PermissionDeniedError(f"{user_role} is not allowed to perform '{action_type}'.")
        return await fn(self, user_role, device_id, action_type, value)

    return wrapper


