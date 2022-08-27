import os
DEFAULT = os.path.join(os.getcwd(),".browser")
class cfDirectory:
    """cfDirectory object
    Handles directories where session tokens, headers, and cookie 
    dumps on CFSession.cfcookie.cfCookieHandler
    
    Basic Usage::
      >>> frp, 
      >>> s = CFSession.cfSession()
      >>> s.get('https://httpbin.org/get')
      <Response [200]>
    Or as a context manager::
      >>> with CFSession.cfSession() as s:
      ...     s.get('https://httpbin.org/get')
      <Response [200]>
    """
    def __init__(self, path: str = DEFAULT, cache_path: str = DEFAULT) -> None:
        self.path = path
        self.cache = cache_path

    def cookie_path(self, name: str = "sitesession.json") -> str:
        if self.path == DEFAULT:
            path = os.path.join(self.path, name)
        else:
            path = os.path.join(self.path, name)
        return path

    def session_path(self, name: str = "session.json") -> str:
        if self.path == DEFAULT:
            path = os.path.join(self.path, name)
        else:
            path = os.path.join(self.path, name)
        return path
    
    def cache_path(self) -> str:
        if self.cache == DEFAULT:
            path = os.path.join(self.path)
        elif set:
            path = self.cache
        return path