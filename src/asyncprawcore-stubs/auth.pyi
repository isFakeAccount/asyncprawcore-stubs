"""Provides Authentication and Authorization classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Awaitable, Callable, ClassVar

from aiohttp.helpers import BasicAuth
from asyncprawcore.codes import codes

if TYPE_CHECKING:
    from aiohttp import ClientResponse
    from asyncprawcore.requestor import Requestor

class BaseAuthenticator(ABC):
    _requestor: Requestor
    client_id: str
    redirect_uri: str | None

    @abstractmethod
    def _auth(self) -> BasicAuth: ...
    def __init__(self, requestor: Requestor, client_id: str, redirect_uri: str | None = None) -> None: ...
    async def _post(self, url: str, success_status: int = codes["ok"], **data: Any) -> ClientResponse: ...
    def authorize_url(self, duration: str, scopes: list[str], state: str, implicit: bool = False) -> str: ...
    async def revoke_token(self, token: str, token_type: str | None = None) -> None: ...

class BaseAuthorizer(ABC):
    AUTHENTICATOR_CLASS: ClassVar[tuple[type, ...] | type]

    def __init__(self, authenticator: BaseAuthenticator) -> None: ...
    def _clear_access_token(self) -> None: ...
    async def _request_token(self, **data: Any) -> None: ...
    def _validate_authenticator(self) -> None: ...
    def is_valid(self) -> bool: ...
    async def revoke(self) -> None: ...

class TrustedAuthenticator(BaseAuthenticator):
    RESPONSE_TYPE: ClassVar[str]

    def __init__(self, requestor: Requestor, client_id: str, client_secret: str, redirect_uri: str | None = None) -> None: ...
    def _auth(self) -> BasicAuth: ...

class UntrustedAuthenticator(BaseAuthenticator):
    def _auth(self) -> BasicAuth: ...

class Authorizer(BaseAuthorizer):
    def __init__(
        self,
        authenticator: BaseAuthenticator,
        *,
        post_refresh_callback: (Callable[[Authorizer], Awaitable[None]] | Callable[[Authorizer], None] | None) = None,
        pre_refresh_callback: (Callable[[Authorizer], Awaitable[None]] | Callable[[Authorizer], None] | None) = None,
        refresh_token: str | None = None,
    ) -> None: ...
    async def authorize(self, code: str) -> None: ...
    async def refresh(self) -> None: ...
    async def revoke(self, only_access: bool = False) -> None: ...

class ImplicitAuthorizer(BaseAuthorizer):
    AUTHENTICATOR_CLASS: ClassVar[type[UntrustedAuthenticator]]  # pyright: ignore [reportIncompatibleVariableOverride]

    def __init__(
        self,
        authenticator: UntrustedAuthenticator,
        access_token: str,
        expires_in: int,
        scope: str,
    ) -> None: ...

class ReadOnlyAuthorizer(Authorizer):
    AUTHENTICATOR_CLASS: ClassVar[type[TrustedAuthenticator]]  # pyright: ignore [reportIncompatibleVariableOverride]
    def __init__(self, authenticator: BaseAuthenticator, scopes: list[str] | None = None) -> None: ...
    async def refresh(self) -> None: ...

class ScriptAuthorizer(Authorizer):
    AUTHENTICATOR_CLASS: ClassVar[type[TrustedAuthenticator]]  # pyright: ignore [reportIncompatibleVariableOverride]

    def __init__(
        self,
        authenticator: BaseAuthenticator,
        username: str | None,
        password: str | None,
        two_factor_callback: Callable | None = None,  # type: ignore
        scopes: list[str] | None = None,
    ) -> None: ...
    async def refresh(self) -> None: ...

class DeviceIDAuthorizer(BaseAuthorizer):
    AUTHENTICATOR_CLASS: ClassVar[tuple[type[TrustedAuthenticator], type[UntrustedAuthenticator]]]  # pyright: ignore [reportIncompatibleVariableOverride]

    def __init__(self, authenticator: BaseAuthenticator, device_id: str | None = None, scopes: list[str] | None = None) -> None: ...
    async def refresh(self) -> None: ...
