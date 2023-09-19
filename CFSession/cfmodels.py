"""
CFSession.cfmodels
~~~~~~~~~~~~~
This module contains the directory options and some supported configurable options
"""


import os
from .cfdefaults import cfConstant
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
        proxy: list = None,
        headless: bool = False,
        ignore_defaults: bool = False,
        chrome_options: uc.ChromeOptions = None,
        desired_capabilities: DesiredCapabilities = None,
    ):
        """Will serve as the configuration options for both the CFSession and the WebDriver Chrome.
        Args:
            proxy (list, optional): A list of proxy server settings. Default is None.
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
        """Reset dcp options to be reused again
           :param defaults: If true, resets it to default (default: True)
        """
        if defaults:
            self.desired_capabilities = self.get_default_dcp()
        #We do nothing since DesiredCapabilities is reusable
        #I added this method just for future use cases

    def reset_chromeoptions(self, defaults = True):
        """Reset chromeoptions to default
           :param defaults: If true, resets it to default (default: True)
        """
        if defaults:
            self.chrome_options = self.get_default_chromeoptions()
        else:
            chrome_old = self.chrome_options.to_capabilities()
            print(chrome_old)

    def get_default_dcp(self):
        "Sets the default options for desired_capabilities and returns it"
        desired_capabilities = DesiredCapabilities().CHROME
        desired_capabilities["pageLoadStrategy"] = "eager"
        return desired_capabilities
    
    def get_default_chromeoptions(self):
        "Sets the default options for chromeoptions and returns it"
        try:
            chrome_options = uc.ChromeOptions()
            chrome_options.use_chromium=True
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-popup-blocking")
        except AttributeError:
            return self.get_default_chromeoptions()
        return chrome_options