"""asyncprawcore.sessions: Provides asyncprawcore.Session and asyncprawcore.session."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, BinaryIO, ClassVar, TextIO

from aiohttp.web import HTTPRequestTimeout
from asyncprawcore.auth import BaseAuthorizer
from asyncprawcore.const import TIMEOUT, WINDOW_SIZE
from asyncprawcore.exceptions import AsyncPrawcoreException

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from asyncprawcore.auth import Authorizer
    from asyncprawcore.requestor import Requestor

log: logging.Logger

class RetryStrategy(ABC):
    @abstractmethod
    def _sleep_seconds(self) -> float | None: ...
    async def sleep(self) -> None: ...

class Session:
    RETRY_EXCEPTIONS: ClassVar[tuple[type[ConnectionError], type[HTTPRequestTimeout]]]
    RETRY_STATUSES: ClassVar[set[int]]
    STATUS_EXCEPTIONS: ClassVar[type[AsyncPrawcoreException]]
    SUCCESS_STATUSES: set[int]

    @staticmethod
    def _log_request(data: list[tuple[str, str]] | None, method: str, params: dict[str, int], url: str) -> None: ...
    @staticmethod
    def _preprocess_dict(data: dict[str, Any]) -> dict[str, str]: ...
    @property
    def _requestor(self) -> Requestor: ...
    async def __aenter__(self) -> Session: ...
    async def __aexit__(self, *_args: Any) -> None: ...
    def __init__(self, authorizer: BaseAuthorizer | None, window_size: int = WINDOW_SIZE) -> None: ...
    async def _do_retry(
        self,
        data: list[tuple[str, Any]],
        json: dict[str, Any],
        method: str,
        params: dict[str, int],
        response: ClientResponse | None,
        retry_strategy_state: FiniteRetryStrategy,
        saved_exception: Exception | None,
        timeout: float,
        url: str,
    ) -> dict[str, Any] | str | None: ...
    async def _make_request(
        self,
        data: list[tuple[str, Any]],
        json: dict[str, Any],
        method: str,
        params: dict[str, Any],
        retry_strategy_state: FiniteRetryStrategy,
        timeout: float,
        url: str,
    ) -> tuple[ClientResponse, None] | tuple[None, Exception]: ...
    def _preprocess_data(
        self,
        data: dict[str, Any],
        files: dict[str, BinaryIO | TextIO] | None,
    ) -> dict[str, str] | None: ...
    def _preprocess_params(self, params: dict[str, int]) -> dict[str, str]: ...
    async def _request_with_retries(
        self,
        data: list[tuple[str, Any]],
        json: dict[str, Any],
        method: str,
        params: dict[str, Any],
        timeout: float,
        url: str,
        retry_strategy_state: FiniteRetryStrategy | None = None,
    ) -> dict[str, Any] | str | None: ...
    async def _set_header_callback(self) -> dict[str, str]: ...
    async def close(self) -> None: ...
    async def request(
        self,
        method: str,
        path: str,
        data: dict[str, Any] | None = None,
        files: dict[str, BinaryIO | TextIO] | None = None,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float = TIMEOUT,
    ) -> dict[str, Any] | str | None: ...

def session(
    authorizer: Authorizer | None = None,
    window_size: int = WINDOW_SIZE,
) -> Session: ...

class FiniteRetryStrategy(RetryStrategy):
    _retries: int

    def __init__(self, retries: int) -> None: ...
    def _sleep_seconds(self) -> float | None: ...
    def consume_available_retry(self) -> FiniteRetryStrategy: ...
    def should_retry_on_failure(self) -> bool: ...
