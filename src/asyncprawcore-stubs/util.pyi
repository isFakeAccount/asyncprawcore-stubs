"""Provide utility for the asyncprawcore package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from asyncprawcore.exceptions import Forbidden, InsufficientScope, InvalidToken

if TYPE_CHECKING:
    from aiohttp import ClientResponse

_auth_error_mapping: dict[int | str, type]

def authorization_error_class(response: ClientResponse) -> InvalidToken | Forbidden | InsufficientScope: ...
