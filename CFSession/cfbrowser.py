"""
CFSession.cfbrowser
~~~~~~~~~~~~~
This module contains the wrapper for Requests
"""
from .cfexception import CFException, CloudflareBlocked, HTTPError, NetworkError, NotFound, URLRequired, TooManyRedirects, Timeout, ConnectTimeout, ReadTimeout
from .cf import CFBypass, SiteBrowserProcess
from .cfdirmodel import cfDirectory    
from .cfdefaults import cfConstant
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
    
    Parameters:
        - directory (cfDirectory, optional): An instance of cfDirectory representing the directory to use. 
                If not provided, a new cfDirectory instance will be created.

        - headless_mode (bool, optional): Whether to run in headless mode (without a graphical user interface). 
            Default is False.

        - tries (int, optional): The number of tries or attempts to bypass cf without human intervention. Default is 3.
                If cf bypass fails, it will automatically revert to providing data from the original, un-bypassed site.

        - *cfarg: Pass arguments to SiteBrowserProcess class (non-keyword arguments).

        - **cfkwarg: Pass keyword arguments to SiteBrowserProcess class.
    """

    

    def __init__(self,directory: cfDirectory = cfDirectory(), headless_mode: bool = False, tries: int = 3,*cfarg, **cfkwarg):
        self.session = requests.Session()
        self.arg = cfarg
        self.kwarg = cfkwarg
        self.headless = headless_mode
        self.directory = directory
        self.cookieChecker = cfSessionHandler(self.directory)
        self._setcookies_status = self.set_cookies()
        self.cf_proccache = None
        self.tries = tries
        self.proxy = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def get(self,url,params=None, **kwargs):
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
    
    def post(self,url,data=None, json=None,**kwargs):
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
    
    def head(self, url, **kwargs):
        r"""Sends a HEAD request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes. If
            `allow_redirects` is not provided, it will be set to `False` (as
            opposed to the default :meth:`request` behavior).
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        kwargs.setdefault("allow_redirects", False)
        return self.request("HEAD", url, **kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        self.url = url
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url,data=None, **kwargs):
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

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("DELETE", url, **kwargs)

    def options(self, url, **kwargs):
        r"""Sends an OPTIONS request.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        kwargs.setdefault("allow_redirects", True)
        return self.request("OPTIONS", url, **kwargs)

    def reload_token(self,site_requested: str,reset=False):
        "Loads cookie, if not found then start bypassing."
        cookieStatus =  self.cookieChecker.cookie_available()
        if not cookieStatus[0] or reset:
            self.cf_proccache = self._class_initialize(site_requested,directory=self.directory,*self.arg,**self.kwarg)
            if reset:
                self.cookieChecker.delete_cookies()
            self.cf_proccache.start()
            self.cf_proccache.close()
        
    def set_cookies(self):
        "Assigns the cookies available on the cache"
        try:
            cookies = json.load(open(self.directory.cookie_path(),"r"))
            selenium_headers = json.load(open(self.directory.session_path(),"r"))
        except FileNotFoundError:
            self.set_agent()
            return False
        self.set_agent(selenium_headers)
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        return True
    
    def set_agent(self, user_agent=cfConstant.USER_AGENT):
        "Sets the user agent of the current session. (Overridden during bypass)"
        self.session.headers.update({"user-agent": user_agent})

    def set_proxy(self, proxy: str):
        """Sets the proxy of the current session. (Will be also used during bypass)
        Format: 'user:pass@localhost:8080' 
        """
        typeofproxy = ...
        self.proxy = {typeofproxy: proxy}

    def _handle_equalfunc(self):
        if not self._setcookies_status:
            self.reload_token(self.url)
            self.set_cookies()

    def request(self,method,url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ) -> requests.Response:
        """Handles bypass automation and returns a response

            :param method: method for the new :class:`Request` object: ``GET``, ``OPTIONS``, ``HEAD``, ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
            :param url: URL for the new :class:`Request` object.
            :param params: (optional) Dictionary, list of tuples or bytes to send
                in the query string for the :class:`Request`.
            :param data: (optional) Dictionary, list of tuples, bytes, or file-like
                object to send in the body of the :class:`Request`.
            :param json: (optional) A JSON serializable Python object to send in the body of the :class:`Request`.
            :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
            :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
            :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart encoding upload.
                ``file-tuple`` can be a 2-tuple ``('filename', fileobj)``, 3-tuple ``('filename', fileobj, 'content_type')``
                or a 4-tuple ``('filename', fileobj, 'content_type', custom_headers)``, where ``'content-type'`` is a string
                defining the content type of the given file and ``custom_headers`` a dict-like object containing additional headers
                to add for the file.
            :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
            :param timeout: (optional) How many seconds to wait for the server to send data
                before giving up, as a float, or a :ref:`(connect timeout, read
                timeout) <timeouts>` tuple.
            :type timeout: float or tuple
            :param allow_redirects: (optional) Boolean. Enable/disable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection. Defaults to ``True``.
            :type allow_redirects: bool
            :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
            :param verify: (optional) Either a boolean, in which case it controls whether we verify
                    the server's TLS certificate, or a string, in which case it must be a path
                    to a CA bundle to use. Defaults to ``True``.
            :param stream: (optional) if ``False``, the response content will be immediately downloaded.
            :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
        """
        content = None
        for t in range(0,self.tries):
            try:
                content = self.session.request(method=method, url=url,
                    params=params,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                    files=files,
                    auth=auth,
                    timeout=timeout,
                    allow_redirects=allow_redirects,
                    proxies=proxies,
                    hooks=hooks,
                    stream=stream,
                    verify=verify,
                    cert=cert,
                    json=json,
                )   
                content.raise_for_status()
                return content
            except requests.exceptions.HTTPError as e:
                http_code = e.response.status_code
                http_content = e.response.content
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
                self.exception = CFException(message=repr(e))
                break
        else:
            caught_code = caught_exception.response.status_code
            if caught_code == 503:
                self.exception = CloudflareBlocked(response=caught_exception.response)
            self.exception = HTTPError(response=caught_exception.response)
        try:
            content.raise_for_status = lambda: self._response_hook_raiseforstatus()
        except AttributeError: #Indicates Response was not created, this usually means that the error is non-HTTP and must be raised immediately
            raise self.exception
        return content    

    def _response_hook_raiseforstatus(self):
        """Raises `CFException` if an error has occured"""
        if isinstance(self.exception,CFException):
                raise self.exception

    def _class_initialize(self,site_requested,directory,*args,**kwargs):
        return SiteBrowserProcess(site_requested,directory=directory,headless_mode=self.headless,*args,**kwargs)
    
    def close(self):
        "Gracefully close a session and closes browser if it has opened."
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
    def __init__(self, directory: cfDirectory = None):
        self.directory = directory
        
    def cookie_available(self):
        if os.path.exists(self.directory.cookie_path()):
            cookie_verified = False
            cookies = json.load(open(self.directory.cookie_path(),"r"))
            for cookie in cookies:
                expiration = int(cookie.get("expiry",False))
                cookie_verified = bool(expiration)
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
        "Initializes the chromedriver and opens the browser"
        self.site = site_requested
        self.cdriver = self._class_initialize(site_requested,directory=self.directory, bypass_mode=self.bypass_mode, *aer, **res)
        self.cdriver.initialize_chromedriver()
        self.cdriver.driver.get(self.site)
        return self.cdriver

    def find(self) -> CFBypass: #returns CFBypass
        "Initializes the bypass engine"
        self.cfinder = CFBypass(self.cdriver.driver, self.directory, bypass_mode=self.bypass_mode)
        return self.cfinder

    def search(self,target_title: Union[str, list] = None):
        """If bypass engine has not been initialized then it will automatically create its own instance. 
        What this does is search for the webpage's title and will keep it open if it is always matching. 
        If the title has changed and no longer matching then it will close the browser and automatically collect the session cookies.
        """
        if not self.cfinder:
            self.cfinder = CFBypass(self.cdriver.driver, self.directory)
        self.cfinder.TARGET_NAME = target_title if target_title != None else self.cfinder.TARGET_NAME
        self.cfinder.start()
