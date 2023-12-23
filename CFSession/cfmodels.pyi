from .cfdefaults import cfConstant as cfConstant
from _typeshed import Incomplete
from typing_extensions import Literal, Tuple, Iterable
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

DEFAULT: str
DEFAULT_NAME: Tuple[Literal["Cookie Name"], Literal["User-Agent Name"]]

class cfDirectory:
    cache: str
    cookie_name: str
    agent_name: str
    chromedriver: str
    def __init__(self, cache_path: str = ..., session_name: Tuple[Literal["Cookie Name"], Literal["User-Agent Name"]]=DEFAULT_NAME, chromedriver_path: str = ...) -> None: ...
    def cookie_path(self) -> str: ...
    def session_path(self) -> str: ...
    def cache_path(self) -> str: ...
    def chromedriver_path(self) -> str: ...

class Proxy:
    dict_proxy: dict
    proxy_address: str
    proxy_hostname: str
    proxy_scheme: str
    proxy_port: int
    username: str
    password: str
    host: str | Iterable[Literal['https','http']]
    dns_on_proxy: bool = True
    def __init__(self, proxy: dict = None, proxy_hostname: str = None, proxy_scheme: str = None, proxy_port: int = None, username: str = None, password: str = None, host: str | Iterable[Literal['https','http']] = ['https','http'], resolve_by_proxy: bool = True) -> None: ...
    def test_proxy(self, protocol: str = ...) -> dict[str, any]: ... 

class Options:
    proxy: Proxy | dict = None
    headless: bool
    ignore_defaults: bool
    chrome_options: uc.ChromeOptions
    desired_capabilities: DesiredCapabilities
    user_agent: str
    ignore_cert_errors: bool
    def __init__(self, proxy: list = ..., headless: bool = ..., chrome_options: uc.ChromeOptions = ..., desired_capabilities: DesiredCapabilities = ..., user_agent: str = ..., ignore_cert_errors: bool = False) -> None: ...
    def reset_dcp(self, defaults: bool = True) -> None: ...
    def reset_chromeoptions(self, defaults: bool = True) -> None: ...
    def get_default_dcp(self) -> DesiredCapabilities: ...
    def get_default_chromeoptions(self) -> uc.ChromeOptions: ...
    def get_proxy_options(self) -> dict[str, Proxy]: ...
    def get_seleniumwire_options(self) -> dict: ...
