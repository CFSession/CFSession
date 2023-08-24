import os
from .cfdefaults import cfConstant

DEFAULT = cfConstant.DEF_DIRECTORY
DEFAULT_NAME = cfConstant.DEF_DIRECTORY_NAME

class cfDirectory:
    """cfDirectory object
    Handles directories where session tokens, headers, and cookie 
    dumps on CFSession.cfcookie.cfCookieHandler
    """
    def __init__(self, cache_path: str = DEFAULT, session_name = DEFAULT_NAME, chromedriver_path: str = None) -> None:
        """
        :param cache_path: Directory where the session cookies and other dumps will be stored.
        :param file_name: Name of the session files Type: `Tuple` (cookie_filename, useragent_filename)
        :param chromedriver_path: Path of the chromedriver
        """
        self.cache = cache_path
        if not isinstance(session_name, tuple): #Guard against invalid arguments
            raise TypeError("Argument session_name must be a tuple")
        self.cookie_name = session_name[0]
        self.agent_name = session_name[1]
        self.chromedriver = chromedriver_path
        
    def cookie_path(self) -> str:
        path = os.path.join(self.cache, self.cookie_name)
        return path

    def session_path(self) -> str:
        path = os.path.join(self.cache, self.agent_name)
        return path
    
    def cache_path(self) -> str:
        "Returns the current patch of "
        return self.cache

    def chromedriver_path(self) -> str:
        "Returns the current path of the chromedriver. Default returns None"
        if self.chromedriver == None:
            return None #default value
        elif self.chromedriver:
            return os.path.join(os.getcwd(), self.chromedriver)