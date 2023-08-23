import requests
from .cf import CFBypass as CFBypass, SiteBrowserProcess as SiteBrowserProcess
from .cfdefaults import cfConstant as cfConstant
from .cfdirmodel import cfDirectory as cfDirectory
from .cfexception import CFException as CFException, CloudflareBlocked as CloudflareBlocked, ConnectTimeout as ConnectTimeout, HTTPError as HTTPError, NetworkError as NetworkError, NotFound as NotFound, ReadTimeout as ReadTimeout, Timeout as Timeout, TooManyRedirects as TooManyRedirects, URLRequired as URLRequired
from _typeshed import Incomplete

from typing_extensions import TypeAlias, Self
from _typeshed import Incomplete, SupportsItems, SupportsRead, Unused
from collections.abc import Callable, Iterable, Mapping, MutableMapping
from typing import Any, Tuple, Union

_Data: TypeAlias = (
    # used in requests.models.PreparedRequest.prepare_body
    #
    # case: is_stream
    # see requests.adapters.HTTPAdapter.send
    # will be sent directly to http.HTTPConnection.send(...) (through urllib3)
    Iterable[bytes]
    # case: not is_stream
    # will be modified before being sent to urllib3.HTTPConnectionPool.urlopen(body=...)
    # see requests.models.RequestEncodingMixin._encode_params
    # see requests.models.RequestEncodingMixin._encode_files
    # note that keys&values are converted from Any to str by urllib.parse.urlencode
    | str
    | bytes
    | SupportsRead[str | bytes]
    | list[tuple[Any, Any]]
    | tuple[tuple[Any, Any], ...]
    | Mapping[Any, Any]
)
RequestsCookieJar = requests.models.cookies.RequestsCookieJar
_Auth: TypeAlias = tuple[str, str] | requests.models.auth.AuthBase | Callable[[requests.PreparedRequest], requests.PreparedRequest]
_Cert: TypeAlias = str | tuple[str, str]
# Files is passed to requests.utils.to_key_val_list()
_FileName: TypeAlias = str | None
_FileContent: TypeAlias = SupportsRead[str | bytes] | str | bytes
_FileContentType: TypeAlias = str
_FileCustomHeaders: TypeAlias = Mapping[str, str]
_FileSpecTuple2: TypeAlias = tuple[_FileName, _FileContent]
_FileSpecTuple3: TypeAlias = tuple[_FileName, _FileContent, _FileContentType]
_FileSpecTuple4: TypeAlias = tuple[_FileName, _FileContent, _FileContentType, _FileCustomHeaders]
_FileSpec: TypeAlias = _FileContent | _FileSpecTuple2 | _FileSpecTuple3 | _FileSpecTuple4
_Files: TypeAlias = Mapping[str, _FileSpec] | Iterable[tuple[str, _FileSpec]]
_Hook: TypeAlias = Callable[[requests.Response], Any]
_HooksInput: TypeAlias = Mapping[str, Iterable[_Hook] | _Hook]

_ParamsMappingKeyType: TypeAlias = str | bytes | int | float
_ParamsMappingValueType: TypeAlias = str | bytes | int | float | Iterable[str | bytes | int | float] | None
_Params: TypeAlias = (
    SupportsItems[_ParamsMappingKeyType, _ParamsMappingValueType]
    | tuple[_ParamsMappingKeyType, _ParamsMappingValueType]
    | Iterable[tuple[_ParamsMappingKeyType, _ParamsMappingValueType]]
    | str
    | bytes
)
_TextMapping: TypeAlias = MutableMapping[str, str]
_HeadersUpdateMapping: TypeAlias = Mapping[str, str | bytes | None]
_Timeout: TypeAlias = float | tuple[float, float] | tuple[float, None]
_Verify: TypeAlias = bool | str


class cfSession:
    session: requests.Session
    arg: Any
    kwarg: Any
    headless: bool
    directory: cfDirectory
    cookieChecker: cfSessionHandler
    cf_proccache: SiteBrowserProcess
    tries: int
    proxy: str
    def __init__(self, directory: cfDirectory = ..., headless_mode: bool = ..., tries: int = ..., *cfarg, **cfkwarg) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(self, *args: Unused) -> None: ...
    url: str
    def get(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> requests.Response: ...
    def post(
            self,
        url: str | bytes,
        data: _Data | None = None,
        json: Incomplete | None = None,
        *,
        params: _Params | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
    ) -> requests.Response: ...
    def head(self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> requests.Response: ...
    def put(
        self,
        url: str | bytes,
        data: _Data | None = None,
        *,
        params: _Params | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> requests.Response: ...
    def patch(
        self,
        url: str | bytes,
        data: _Data | None = None,
        *,
        params: _Params | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> requests.Response: ...
    def delete(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> requests.Response: ...
    def options(
        self,
        url: str | bytes,
        *,
        params: _Params | None = ...,
        data: _Data | None = ...,
        headers: _HeadersUpdateMapping | None = ...,
        cookies: RequestsCookieJar | _TextMapping | None = ...,
        files: _Files | None = ...,
        auth: _Auth | None = ...,
        timeout: _Timeout | None = ...,
        allow_redirects: bool = ...,
        proxies: _TextMapping | None = ...,
        hooks: _HooksInput | None = ...,
        stream: bool | None = ...,
        verify: _Verify | None = ...,
        cert: _Cert | None = ...,
        json: Incomplete | None = ...,
    ) -> requests.Response: ...
    def reload_token(self, site_requested: str, reset: bool = ...) -> None: ...
    def set_cookies(self) -> bool: ...
    def set_agent(self, user_agent=...) -> None: ...
    def set_proxy(self, proxy: str) -> None: ...
    exception: Incomplete
    def request(self,
        method: str | bytes,
        url: str | bytes,
        params: _Params | None = None,
        data: _Data | None = None,
        headers: _HeadersUpdateMapping | None = None,
        cookies: None | RequestsCookieJar | _TextMapping = None,
        files: _Files | None = None,
        auth: _Auth | None = None,
        timeout: _Timeout | None = None,
        allow_redirects: bool = True,
        proxies: _TextMapping | None = None,
        hooks: _HooksInput | None = None,
        stream: bool | None = None,
        verify: _Verify | None = None,
        cert: _Cert | None = None,
        json: Incomplete | None = None,
    ) -> requests.Response: ...
    def close(self) -> None: ...

class cfSessionHandler:
    directory: cfDirectory
    def __init__(self, directory: cfDirectory = ...) -> None: ...
    def cookie_available(self) -> Tuple[bool,str]: ...
    def delete_cookies(self) -> None: ...

class cfSimulacrum(cfSession):
    cdriver: SiteBrowserProcess
    cfinder: CFBypass
    site: str
    bypass_mode: bool
    def __init__(self, *aer, **res) -> None: ...
    def copen(self, site_requested, *aer, **res) -> SiteBrowserProcess: ...
    def find(self) -> CFBypass: ...
    def search(self, target_title: Union[str, list] = ...): ...