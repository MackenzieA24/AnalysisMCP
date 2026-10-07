from __future__ import annotations

import functools
import inspect
from datetime import datetime
from typing import Any


def parse_date(value: str | None) -> str | None:
    if value in (None, ""):
        return None
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(candidate).date().isoformat()
    except ValueError:
        return value


def normalise_model_name(value: Any) -> str:
    if value is None:
        return "Unknown"
    return str(value)


def safe_tool_call(fn):
    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def async_wrapper(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except Exception as exc:  # pragma: no cover - safety layer for MCP tools  # noqa: BLE001
                return {"ok": False, "error": str(exc)}

        return async_wrapper

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # pragma: no cover - safety layer for MCP tools  # noqa: BLE001
            return {"ok": False, "error": str(exc)}

    return wrapper
