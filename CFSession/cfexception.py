"""
CFSession.cfexception
~~~~~~~~~~~~~
This module contains the exceptions for CFSession
"""

class CFException(Exception): #Parent class
    def __init__(self,message=None,response=None,request=None, *args, **kwargs):
        """There was an ambiguous exception that occurred while handling your
    request."""
        super().__init__(message,*args, **kwargs)
        self.response = response



class NetworkError(CFException): #Main class
    def __init__(self, response=None,*args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class HTTPError(CFException): #Main class
    def __init__(self, response=None, *args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class NotFound(HTTPError): #Subclass
    #subclass
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class CloudflareBlocked(HTTPError): #Subclass
    #subclass
    def __init__(self, response=None, *args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class URLRequired(CFException): #Main class
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class TooManyRedirects(CFException): #Main class
    def __init__(self, response, *args, **kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class Timeout(CFException): #Main class
    def __init__(self, response=None, *args,**kwargs):
        default_message = repr(response)
        super().__init__(default_message,response=response, *args, **kwargs)

class ConnectTimeout(Timeout): #Subclass
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

class ReadTimeout(Timeout): #Subclass
    def __init__(self, response=None,*args, **kwargs):
        # if any arguments are passed...
        # If you inherit from the exception that takes message as a keyword
        # maybe you will need to check kwargs here
        super().__init__(response=response, *args, **kwargs)

