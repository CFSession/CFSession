"""
CFSession.cfmodels
~~~~~~~~~~~~~
This module contains the directory options and some supported configurable options
"""

import os
from typing import Union, Iterable, Literal
from .cfdefaults import cfConstant
from .cfexception import ProxyConfigurationError, ProxyDecodeError
import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from collections import UserDict
import requests
import re

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
            - cache_path: Directory where the session cookies and other dumps will be stored.
            - session_name: Name of the session files Type: `Tuple` (cookie_filename, useragent_filename)
            - chromedriver_path: Path of the chromedriver
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

class Proxy(UserDict):
    """Proxy Manager for cfSession
    Handles proxy configurations.
    """
    def __init__(self, 
        proxy: dict = None, 
        proxy_hostname: str = None,
        proxy_scheme: str = None, 
        proxy_port: int = None , 
        username: str = None, 
        password: str = None, 
        host: Union[str, Iterable[Literal['https','http']]] = ['https','http'],
        resolve_by_proxy: bool = True
    ) -> None:
        """Args:
        - proxy (dict): A dictionary containing proxy details. If provided, individual proxy details should not be specified.
        - proxy_hostname (str): The hostname or IP address of the proxy.
        - proxy_scheme (str): The protocol your proxy is using
        - proxy_port (int): The port number of the proxy.
        - username (str): The username for proxy authentication.
        - password (str): The password for proxy authentication.
        - host (str, Iterable): The protocol or host target for the proxy (e.g., 'http', 'https')
        - resolve_by_proxy (bool): Resolve DNS by proxy when using socks5.
        
        If 'proxy' is provided, it takes precedence over individual proxy details. If 'proxy' is not provided,
        'proxy_hostname' and 'proxy_port' must be specified.
        
        Proxy format for proxy parameter: 
        `{'{Scheme/Host Target}': '{proxyProtocol}://{username}:{password}@{hostname}:{PORT}'}`
        
        Example:
        ```py
            proxy = Proxy({'https': 'socks5://user:password123@hostname.com:3234'})
            Options(proxy=proxy)
        ```
        """
        #Guard against invalid configurations
        if not isinstance(proxy, dict) and proxy is not None:
            raise ValueError("The 'proxy' argument must be a dictionary.")
        elif proxy and any((proxy_hostname, proxy_port, proxy_scheme)):
            raise ProxyConfigurationError("Either provide the 'proxy' argument or specify 'proxy_hostname', 'proxy_scheme', 'proxy_port' individually.")
        self.data = {}
        self.host = host
        self.dns_on_proxy = resolve_by_proxy
        if proxy:
            self.data = proxy
            self.proxy_address = list(proxy.values())[0]
            #Extract values
            match = re.match(r'^(?P<scheme>\w+)://(?:((?P<username>\w+):(?P<password>\w+)@)|(?P<username_only>\w+)@)?(?P<hostname>[\w.]+):(?P<port>\d+)$', self.proxy_address)
            if not match:
                raise ProxyDecodeError('Your proxy format is invalid')
            self.proxy_scheme = match.group('scheme')
            self.proxy_hostname = match.group('hostname')
            self.proxy_port = int(match.group('port'))
            self.username = match.group('username') or match.group('username_only')
            self.password = match.group('password')
        elif any((proxy_hostname, proxy_port, proxy_scheme)):
            #Guard against invalid configurations again
            if not proxy_hostname:
                raise ProxyConfigurationError("'proxy_hostname' is empty")
            if not proxy_scheme:
                raise ProxyConfigurationError("'proxy_scheme' is empty")
            if not proxy_port:
                raise ProxyConfigurationError("'proxy_port' is empty")
            self.proxy_hostname = proxy_hostname
            self.proxy_scheme = proxy_scheme
            self.proxy_port = proxy_port
            self.username = username
            self.password = password
            credformat = f"{self.username}:{self.password}@" if self.username and self.password else ""
            self.proxy_address = f"{self.proxy_scheme}://{credformat}{self.proxy_hostname}:{proxy_port}"
            if isinstance(self.host, Iterable):
                for host in self.host:
                    self.data[host] = self.proxy_address
            else:
                self.data = {self.host: self.proxy_address}
        else:
            self.data = {}
            self.proxy_address = ''
        #Final touch
        if self.dns_on_proxy:
            self.proxy_address = self.proxy_address.replace('socks5', 'socks5h')
    
    def test_proxy(self, protocol = 'https', demo = True):
        """Tests if a proxy is working properly, returns detail of your setup and the collected ip.
        Args:
        - demo (bool, optional): Demonstration mode, Redacted configuration if True. 
        """
        url = f'{protocol}://httpbin.org/ip'
        try:
            response=requests.get(url, proxies=self)
            response.raise_for_status()
            decoded_resp = response.json()
        except requests.exceptions.HTTPError as e:
            decoded_resp = {
                'origin': False,
                'response': e.response
            }
        except requests.exceptions.RequestException as e:
            decoded_resp = {
                'origin': False,
                'exception': e
            }
        configuration = self
        if demo:
            configuration = '[REDACTED]'
        return {'result': decoded_resp, 
                'url': url, 
                'protocol': protocol, 
                'config': configuration}

class Options:
    """Options object
    Handles the options, default settings and configuration that will be used on both uc.Chrome() and cfSession
    """
    def __init__(self,
        proxy: Union[Proxy, dict] = None,
        headless: bool = False,
        ignore_defaults: bool = False,
        chrome_options: uc.ChromeOptions = None,
        desired_capabilities: DesiredCapabilities = None,
        user_agent: str = None,
        ignore_cert_errors: bool = False
    ):
        """Will serve as the configuration options for both the CFSession and the WebDriver Chrome.
        Args:
            - proxy (list, optional):\
                proxy server setting. Example:\
                `{\
                    "https": "https://ip:port"\
                }`
                Supported protocols: http, https, ftp, socks5 `http: 'socks5://ip:port'`
            - headless (bool, optional): Whether to run the browser in headless mode (no GUI). Default is False.
            - ignore_defaults (bool, optional): Whether to ignore default settings. Default is False.
            - chrome_options (uc.ChromeOptions, optional): Custom Chrome options to configure the browser.
            - desired_capabilities (DesiredCapabilities, optional): Desired capabilities for the WebDriver session.
            - user_agent (str, optional): Sets the user agent of the current sesssion.
            - ignore_cert_errors (bool, optional): Ignores certificate errors

        Note:
            - `proxy` should be a list of dictionaries with proxy server settings.
            - `chrome_options` should be an instance of `uc.ChromeOptions`.
            - `desired_capabilities` should be an instance of `DesiredCapabilities`.
        """
        if isinstance(proxy, dict):
            self.proxy = Proxy(proxy)
        elif isinstance(proxy, Proxy):
            self.proxy = proxy
        else:
            self.proxy = proxy
        self.headless = headless
        self.user_agent = user_agent
        self.ignore_cert_errors = ignore_cert_errors
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
        if self.user_agent:
            chrome_options.add_argument("--user-agent=%s" % self.user_agent)
        if self.ignore_cert_errors:
            chrome_options.add_argument("--ignore-certificate-errors-spki-list")
            chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.no_sandbox = False
        return chrome_options
    
    def get_proxy_options(self):
        "selenium-wire proxy options"
        if self.proxy:
            return {
                'proxy': self.proxy,
                'no_proxy': 'localhost,127.0.0.1'
            }
        return {}
    
    def get_seleniumwire_options(self):
        "selenium-wire specific options"
        swire_options = {}
        swire_options.update(self.get_proxy_options())
        return swire_options