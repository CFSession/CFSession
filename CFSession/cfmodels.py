"""
CFSession.cfmodels
~~~~~~~~~~~~~
This module contains the directory options and some supported configurable options
"""


import os
from .cfdefaults import cfConstant
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy

DEFAULT = cfConstant.DEF_DIRECTORY
DEFAULT_NAME = cfConstant.DEF_DIRECTORY_NAME

class cfDirectory:
    """cfDirectory object
    Handles directories where session tokens, headers, and cookie 
    dumps on CFSession.cfcookie.cfCookieHandler
    """
    def __init__(self, cache_path: str = DEFAULT, session_name = DEFAULT_NAME, chromedriver_path: str = None) -> None:
        """
        Args:
            cache_path: Directory where the session cookies and other dumps will be stored.
            session_name: Name of the session files Type: `Tuple` (cookie_filename, useragent_filename)
            chromedriver_path: Path of the chromedriver
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
        "Returns the current path of the cache directory." 
        return self.cache

    def chromedriver_path(self) -> str:
        "Returns the current path of the chromedriver. Default is None"
        if self.chromedriver == None:
            return None #default value
        elif self.chromedriver:
            return os.path.join(os.getcwd(), self.chromedriver)

class Options:
    """Options object
    Handles the options, default settings and configuration that will be used on both uc.Chrome() and cfSession
    """
    def __init__(self,
        proxy: dict = {},
        headless: bool = False,
        ignore_defaults: bool = False,
        chrome_options: uc.ChromeOptions = None,
        desired_capabilities: DesiredCapabilities = None,
    ):
        """Will serve as the configuration options for both the CFSession and the WebDriver Chrome.
        Args:
            proxy (list, optional):\
                proxy server setting. Example:\
                `{\
                    "https": "https://ip:port"\
                }`
                Supported protocols: http, https, ftp, socks5 `http: 'socks5://ip:port'`
            headless (bool, optional): Whether to run the browser in headless mode (no GUI). Default is False.
            ignore_defaults (bool, optional): Whether to ignore default settings. Default is False.
            chrome_options (uc.ChromeOptions, optional): Custom Chrome options to configure the browser.
            desired_capabilities (DesiredCapabilities, optional): Desired capabilities for the WebDriver session.

        Note:
            - `proxy` should be a list of dictionaries with proxy server settings.
            - `chrome_options` should be an instance of `uc.ChromeOptions`.
            - `desired_capabilities` should be an instance of `DesiredCapabilities`.
        """
        self.proxy = proxy
        self.headless = headless
        self.ignore_defaults = ignore_defaults
        self.chrome_options = chrome_options if chrome_options else self.get_default_chromeoptions()
        self.desired_capabilities = desired_capabilities if desired_capabilities else self.get_default_dcp()

    def reset_dcp(self, defaults = True):
        """Reset `desired_capabilities` argument to be reused again
           :param defaults: If true, resets it to default (default: True)
        """
        if defaults:
            self.desired_capabilities = self.get_default_dcp()
        #We do nothing since DesiredCapabilities is reusable
        #I added this method just for future use cases

    def reset_chromeoptions(self, defaults = True):
        """Reset `chrome_options` argument to be reused again
           :param defaults: If true, resets it to default (default: True)
        """
        if defaults:
            self.chrome_options = self.get_default_chromeoptions()
        else:
            chrome_old_args = self.chrome_options.arguments
            self.chrome_options = uc.ChromeOptions()
            self.chrome_options._arguments = chrome_old_args
            
    def get_default_dcp(self):
        "Sets the default options for desired_capabilities and returns it"
        desired_capabilities = DesiredCapabilities().CHROME.copy()
        desired_capabilities["pageLoadStrategy"] = "eager"
        return desired_capabilities
    
    def get_default_chromeoptions(self):
        "Sets the default options for chromeoptions and returns it"
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.no_sandbox = False
        if self.proxy:
            proxy_http = self.proxy.get('http', None) or self.proxy.get('https', None) or self.proxy.get('ftp', None)
            proxy = Proxy()
            if self.proxy.get('http'):
                proxy.http_proxy = proxy_http
            elif self.proxy.get('https'):
                proxy.ssl_proxy = proxy_http
            elif self.proxy.get('ftp'):
                proxy.ftp_proxy = proxy_http
            else:
                proxy.auto_detect = proxy_http
            chrome_options.proxy = proxy
        return chrome_options