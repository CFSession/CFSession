"""
CFSession.cfbrowser
~~~~~~~~~~~~~
This module contains the wrapper for Requests
"""
from .cfexception import CFException, CloudflareBlocked, HTTPError, NetworkError, NotFound, URLRequired, TooManyRedirects, Timeout, ConnectTimeout, ReadTimeout
from .cf import CFBypass, SiteBrowserProcess
from .cfdirmodel import cfDirectory    
from datetime import timezone
import requests
import datetime
from typing import Union
import json
import os


class cfSession():
    """cfSession object
    A modified Requests session.
    Provides everything a requests.Session can do.
    Is able to establish connection to sites under IUAM 
    
    Basic Usage::
      >>> import CFSession
      >>> s = CFSession.cfSession()
      >>> s.get('https://httpbin.org/get')
      <Response [200]>
    Or as a context manager::
      >>> with CFSession.cfSession() as s:
      ...     s.get('https://httpbin.org/get')
      <Response [200]>
    """

    def __init__(self,directory: cfDirectory = cfDirectory(),*cfarg, **cfkwarg):
        self.session = requests.Session()
        self.arg = cfarg
        self.kwarg = cfkwarg
        self.directory = directory
        self.cookieChecker = cfSessionHandler(self.directory)
        self._setcookies_status = self.set_cookies()
        self.cf_proccache = None
        self.bypass_mode = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def get(self,url,params=None, **kwargs) -> requests.Response:
        r"""Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("GET", url, params=params, **kwargs)
    
    def post(self,url,data=None, json=None,**kwargs) -> requests.Response:
        r"""Sends a POST request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        self.url = url
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs) -> requests.Response:
        r"""Sends a PUT request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        self.url = url
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url,data=None, **kwargs) -> requests.Response:
        r"""Sends a PATCH request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs) -> requests.Response:
        r"""Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("DELETE", url, **kwargs)

    def reload_token(self,site_requested,reset=False):
        cookieStatus =  self.cookieChecker.cookie_available()
        if not cookieStatus[0] or reset:
            self.cf_proccache = self._class_initialize(site_requested,directory=self.directory,*self.arg,**self.kwarg)
            if reset:
                self.cookieChecker.delete_cookies()
            self.cf_proccache.bypass_mode = self.bypass_mode
            self.cf_proccache.start()
            self.cf_proccache.close()
        
    def set_cookies(self):
        try:
            cookies = json.load(open(self.directory.cookie_path(),"r"))
            selenium_headers = json.load(open(self.directory.session_path(),"r"))
        except FileNotFoundError:
            return False
        self.session.headers.update({"user-agent": selenium_headers})
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        return True

    def _handle_equalfunc(self):
        if not self._setcookies_status:
            self.reload_token(self.url)
            self.set_cookies()

    def request(self,method,url,**kwargs) -> requests.Response:
        content = None
        for t in range(0,2):
            try:
                if method == "GET":
                    content = self.session.get(url, **kwargs)
                elif method == "POST":
                    content = self.session.post(url, **kwargs)
                elif method == "PATCH":
                    content = self.session.patch(url, **kwargs)
                elif method == "PUT":
                    content = self.session.put(url, **kwargs)
                elif method == "DELETE":
                    content = self.session.delete(url, **kwargs)
                content.raise_for_status()
                return content
            except requests.exceptions.HTTPError as e:
                http_code = e.response.status_code
                caught_exception = e
                if http_code == 404:
                    self.exception = NotFound(response=e.response)
                    break
                elif http_code == 503:
                    #CF blocked us, update the token
                    #Recheck token
                    self.reload_token(url,reset=True)
                    self.set_cookies()
                elif http_code == 403:
                    #Different blocking method, usually its an IUAM javascript challenge but sometimes a recaptcha
                    self.reload_token(url,reset=True)
                    self.set_cookies()
                continue
            except requests.exceptions.ConnectionError as e:
                caught_exception = e
                self.exception = NetworkError(response=e.response)
                break
            except requests.exceptions.URLRequired as e:
                self.exception = URLRequired(response=e.response)
                break
            except requests.exceptions.TooManyRedirects as e:
                self.exception = TooManyRedirects(response=e.response)
                break
            except requests.exceptions.Timeout as e:
                self.exception = Timeout(response=e.response)
                break
            except requests.exceptions.RequestException as e: #When an arbitrary error occurs
                self.exception = CFException(response=e.response)
                break
        else:
            caught_code = caught_exception.response.status_code
            if caught_code == 503:
                self.exception = CloudflareBlocked(response=caught_exception.response)
            self.exception = HTTPError(response=caught_exception.response)
        try:
            content.raise_for_status = lambda: self._response_hook_raiseforstatus(content)
        except AttributeError: #Indicates Response was not created, this usually means that the error is non-HTTP and must be raised immediately
            raise self.exception
        return content    

    def _response_hook_raiseforstatus(self, objself: CFException):
        """Raises `CFException` if an error has occured"""
        if isinstance(self.exception,CFException):
                raise self.exception

    def _class_initialize(self,site_requested,directory,*args,**kwargs):
        return SiteBrowserProcess(site_requested,directory=directory,*args,**kwargs)

    def close(self):
        self.session.close()
        if self.cf_proccache:
            self.cf_proccache.close()
            del self.cf_proccache

    def __repr__(self):
        return "<cfSession Object>"
    
    def __getstate__(self):
        state = {attr: getattr(self, attr, None) for attr in self.__attrs__}
        return state
    
    def __setstate__(self, state):
        for attr, value in state.items():
            setattr(self, attr, value)


class cfSessionHandler:
    def __init__(self, directory: cfDirectory = None) -> None:
        self.directory = directory
        
    def cookie_available(self):
        if os.path.exists(self.directory.cookie_path()):
            cookie_verified = False
            cookies = json.load(open(self.directory.cookie_path(),"r"))
            for cookie in cookies:
                expirey = cookie.get("expiry",False)
                if expirey != False:
                    cookie_verified = True
                    expiration = int(expirey)
                else:
                    pass
            if not cookie_verified:    
                return (True, "Token validity unconfirmed")
            # epoch_time = int(time.time())
            dt = datetime.datetime.now(timezone.utc)
            utc_time = dt.replace(tzinfo=timezone.utc).replace(microsecond=0)
            epoch_time = int(utc_time.timestamp())
            if epoch_time >= expiration:
                return (False, "Token has expired")      
            if not os.path.exists(self.directory.session_path()):
                return (False, "Header is not found")
            return (True, "Available")
        return (False, "No cookie found")
    
    def delete_cookies(self):
        try:
            os.remove(self.directory.cookie_path())
        except OSError:
            pass

class cfSimulacrum(cfSession):
    def __init__(self, *aer, **res):
        super().__init__(*aer,**res)
        self.cdriver = None
        self.cfinder = None
        self.site = None
        self.bypass_mode = False
        
    def copen(self, site_requested, *aer, **res) -> SiteBrowserProcess: # returns SiteBrowserProcess
        self.site = site_requested
        self.cdriver = self._class_initialize(site_requested,directory=self.directory, *aer, **res)
        self.cdriver._init_chromedriver_manual() 
        self.cdriver.driver.get(self.site)
        return self.cdriver

    def find(self) -> CFBypass: #returns CFBypass
        self.cfinder = CFBypass(self.cdriver.driver, self.directory)
        return self.cfinder

    def search(self,target_title: Union[str, list] = None):
        if not self.cfinder:
            self.cfinder = CFBypass(self.cdriver.driver, self.directory)
        self.cfinder.TARGET_NAME = target_title if target_title != None else self.cfinder.TARGET_NAME
        self.cfinder.start()
