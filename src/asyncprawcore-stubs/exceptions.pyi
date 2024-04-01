"""Provide exception classes for the asyncprawcore package."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aiohttp import ClientResponse

class AsyncPrawcoreException(Exception): ...
class InvalidInvocation(AsyncPrawcoreException): ...

class OAuthException(AsyncPrawcoreException):
    response: ClientResponse
    error: str
    description: str | None

    def __init__(self, response: ClientResponse, error: str, description: str | None = None) -> None: ...

class RequestException(AsyncPrawcoreException):
    original_exception: Exception
    request_args: tuple[Any, ...]
    request_kwargs: dict[str, bool | dict[str, int] | dict[str, str] | str | None]

    def __init__(
        self,
        original_exception: Exception,
        request_args: tuple[Any, ...],
        request_kwargs: dict[str, bool | dict[str, int] | dict[str, str] | str | None],
    ) -> None: ...

class ResponseException(AsyncPrawcoreException):
    response: ClientResponse

    def __init__(self, response: ClientResponse) -> None: ...

class BadJSON(ResponseException): ...
class BadRequest(ResponseException): ...
class Conflict(ResponseException): ...
class Forbidden(ResponseException): ...
class InsufficientScope(ResponseException): ...
class InvalidToken(ResponseException): ...
class NotFound(ResponseException): ...

class Redirect(ResponseException):
    path: str
    response: ClientResponse

    def __init__(self, response: ClientResponse) -> None: ...

class ServerError(ResponseException): ...

class SpecialError(ResponseException):
    response: ClientResponse
    message: str
    reason: str
    special_errors: list[Any]

    def __init__(self, response: ClientResponse, resp_dict: dict[str, Any]) -> None: ...

class TooLarge(ResponseException): ...

class TooManyRequests(ResponseException):
    retry_after: Optional[int]
    response: ClientResponse
    message: str

    def __init__(self, response: ClientResponse) -> None: ...

class URITooLong(ResponseException): ...
class UnavailableForLegalReasons(ResponseException): ...
