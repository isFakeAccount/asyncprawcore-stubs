"""Provides the HTTP request handling interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiohttp import ClientSession
from asyncprawcore.const import TIMEOUT

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop

    from aiohttp import ClientResponse

class Requestor:
    loop: AbstractEventLoop
    _http: ClientSession
    oauth_url: str
    reddit_url: str
    timeout: float

    def __getattr__(self, attribute: str) -> Any: ...
    def __init__(
        self,
        user_agent: str,
        oauth_url: str = "https://oauth.reddit.com",
        reddit_url: str = "https://www.reddit.com",
        session: ClientSession | None = None,
        loop: AbstractEventLoop | None = None,
        timeout: float = TIMEOUT,
    ) -> None: ...
    async def close(self) -> None: ...
    async def request(self, *args: Any, timeout: float | None = None, **kwargs: Any) -> ClientResponse: ...
