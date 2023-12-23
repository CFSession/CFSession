"""
CFSession.cfexception
~~~~~~~~~~~~~
This module contains the exceptions for CFSession
"""

class CFException(Exception): #Parent class
    def __init__(self,message=None,response=None,request=None, *args, **kwargs):
        """There was an ambiguous exception that occurred while handling your
    request."""
        self.response = response
        message = repr(response) if not message else message
        super().__init__(message,*args, **kwargs)



class NetworkError(CFException): #Main class
    "Network error had occured"
    def __init__(self, response=None,*args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class HTTPError(CFException): #Main class
    "HTTP related error had occured"
    def __init__(self, response=None, *args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class NotFound(HTTPError): #Subclass
    "HTTP-404 Not found error had occured"
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class CloudflareBlocked(HTTPError): #Subclass
    "Blocked by Cloudflare"
    def __init__(self, response=None, *args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class URLRequired(CFException): #Main class
    "URL Required error"
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class TooManyRedirects(CFException): #Main class
    "Too Many Redirects error"
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class Timeout(CFException): #Main class
    "Timeout Error"
    def __init__(self, response=None, *args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class ConnectTimeout(Timeout): #Subclass
    "Connection Timeout error"
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class ReadTimeout(Timeout): #Subclass
    "Read Timeout error"
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class ProxyError(CFException): #Main class:
    "Proxy related errors"
    def __init__(self, message=None, response=None, request=None, *args, **kwargs):
        super().__init__(message, response, request, *args, **kwargs)

class ProxyConfigurationError(ProxyError): #Sub class:
    "Proxy Configuration error"
    def __init__(self, message=None, response=None, request=None, *args, **kwargs):
        super().__init__(message, response, request, *args, **kwargs)

class ProxyDecodeError(ProxyError): #Sub class:
    "Proxy Decode error"
    def __init__(self, message=None, response=None, request=None, *args, **kwargs):
        super().__init__(message, response, request, *args, **kwargs)