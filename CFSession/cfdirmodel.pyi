from ..CFSession.cfdefaults import cfConstant as cfConstant
from _typeshed import Incomplete
from typing_extensions import Literal, Tuple

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
