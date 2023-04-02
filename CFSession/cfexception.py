"""
CFSession.cfexception
~~~~~~~~~~~~~
This module contains the exceptions for CFSession
"""

class CFException(Exception):
    def __init__(self,message=None,response=None,request=None, *args, **kwargs):
        """There was an ambiguous exception that occurred while handling your
    request."""
        super().__init__(message,*args, **kwargs)
        self.response = response



class NetworkError(CFException):
    def __init__(self, response=None,*args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class HTTPError(CFException):
    def __init__(self, response=None, *args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class NotFound(HTTPError): 
    #subclass
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class CloudflareBlocked(HTTPError):
    #subclass
    def __init__(self, response=None, *args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class URLRequired(CFException):
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class TooManyRedirects(CFException):
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class Timeout(CFException):
    """The request timed out.

    Catching this error will catch both
    :exc:`~requests.exceptions.ConnectTimeout` and
    :exc:`~requests.exceptions.ReadTimeout` errors.
    """

    pass

class ConnectTimeout(Timeout):
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class ReadTimeout(Timeout):
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

