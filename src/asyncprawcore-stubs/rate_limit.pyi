"""Provide the RateLimiter class."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Mapping

log: logging.Logger

if TYPE_CHECKING:
    from aiohttp import ClientResponse

class RateLimiter:
    remaining: float | None
    next_request_timestamp: float | None
    reset_timestamp: float | None
    used: int | None
    window_size: int

    def __init__(self, *, window_size: int) -> None: ...
    async def call(
        self,
        request_function: Callable[
            [Any],
            Awaitable[ClientResponse],
        ],
        set_header_callback: Callable[[], Awaitable[dict[str, str]]],
        *args: Any,
        **kwargs: Any,
    ) -> ClientResponse: ...
    async def delay(self) -> None: ...
    def update(self, response_headers: Mapping[str, str]) -> None: ...
