"""
CFSession.cfexception
~~~~~~~~~~~~~
This module contains the exceptions for CFSession
"""

class CFException(Exception):
    def __init__(self, *args, **kwargs):
        """There was an ambiguous exception that occurred while handling your
    request."""
        response = kwargs.pop("response", None)
        self.response = response
        self.request = kwargs.pop("request", None)
        if response is not None and not self.request and hasattr(response, "request"):
            self.request = self.response.request
        super().__init__(*args, **kwargs)


class NotFound(CFException):
     def __init__(self,response=None, *args, **kwargs):
        default_message = repr(response)
        self.response = response.response

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
        default_message = repr(response)
        self.response = response.response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class HTTPError(CFException):
    def __init__(self,response = None,*args,**kwargs):
        default_message = repr(response)
        self.response = response.response

        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class CloudflareBlocked(CFException):
    def __init__(self,response,*args,**kwargs):
        default_message = repr(response)
        self.response = response.response

        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class URLRequired(CFException):
    def __init__(self,response,*args,**kwargs):
        default_message = repr(response)
        self.response = response.response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class TooManyRedirects(CFException):
    def __init__(self,response,*args,**kwargs):
        default_message = repr(response)
        self.response = response.response
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
    def __init__(self,response,*args,**kwargs):
        default_message = repr(response)
        self.response = response.response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

class ReadTimeout(Timeout):
    def __init__(self,response,*args,**kwargs):
        default_message = repr(response)
        self.response = response.response
        if args:
            # ... pass them to the super constructor
            super().__init__(*args, **kwargs)
        else: # else, the exception was raised without arguments ...
                 # ... pass the default message to the super constructor
            super().__init__(default_message, **kwargs)

