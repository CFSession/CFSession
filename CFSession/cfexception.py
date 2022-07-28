
from sqlite3 import Time
from urllib import response


class CFException(Exception):
    def __init__(self, *args, **kwargs):
        """Initialize RequestException with `request` and `response` objects."""
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request
        super().__init__(*args, **kwargs)


class NotFound(CFException):
     def __init__(self,response=None, *args, **kwargs):
        default_message = 'Not Found'
        self.code = 404

        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class NetworkError(CFException):
    def __init__(self,response=None,*args,**kwargs):
        default_message = 'There has been a connection error'
        self.response = response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class HTTPError(CFException):
    def __init__(self,code,content,*args,**kwargs):
        default_message = 'There has been an HTTP error'
        self.code = code
        self.content = content

        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class CloudflareBlocked(CFException):
    def __init__(self,code,content,*args,**kwargs):
        default_message = 'CF has persistently blocked us, please report this issue.'
        self.status_code = code
        self.content = content

        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class URLRequired(CFException):
    def __init__(self,response=None,*args,**kwargs):
        default_message = 'A valid URL is required to make a request.'
        self.response = response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class TooManyRedirects(CFException):
    def __init__(self,response,*args,**kwargs):
        default_message = 'Too many redirects'
        self.response = response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class Timeout(CFException):
    """The request timed out.

    Catching this error will catch both
    :exc:`~requests.exceptions.ConnectTimeout` and
    :exc:`~requests.exceptions.ReadTimeout` errors.
    """

    pass

class ConnectTimeout(Timeout):
    def __init__(self,response=None,*args,**kwargs):
        default_message = 'The request timed out while trying to connect to the remote server.'
        self.response = response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class ReadTimeout(Timeout):
    def __init__(self,response=None,*args,**kwargs):
        default_message = 'The server did not send any data in the allotted amount of time.'
        self.response = response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

