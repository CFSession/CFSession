"""
CFSession.cfdefaults
~~~~~~~~~~~~~
This module contains the default parameters on CFSession.cf.SiteBrowserProcess 
for the UC(undetected chromium) process
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Required_defaults:
    """
    This the class where you can modify "options" and "DesiredCapabilities" without affecting the default settings

    Basic Usage::
      >>> import CFSession
      >>> defaults = CFSession.Required_defaults()
      >>> defaults.options = uc.ChromeOptions #You can modify options here
      >>> defaults.dcp = DesiredCapabilities().CHROME #You can modify DesiredCapabilites
      >>> CFSession.cf.SiteBrowserProcess(ignore_defaults=True,defaults=defaults)
    
    Since ChromeOptions cannot be reused:
      `Required_defaults.reset_objects()`
      will fix this issue
    """
    def __init__(self) -> None:
        self.options = None
        self.dcp = None

    def reset_objects(self, default = True) -> None:
        #reset current state 
        self.options = uc.ChromeOptions()
        self.dcp = DesiredCapabilities().CHROME

    def options_default(self) -> uc.ChromeOptions():
        try:
            self.options.use_chromium=True
            self.options.add_argument("--disable-renderer-backgrounding")
            self.options.add_argument("--disable-backgrounding-occluded-windows")
            self.options.add_argument("--disable-popup-blocking")

        except AttributeError:
            self.reset_objects()
            return self.options_default()
        return self.options

    def desired_capabilites_default(self) -> DesiredCapabilities:
        self.dcp["pageLoadStrategy"] = "eager"
        return self.dcp

class cfConstant:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    DEBUG_DUMMY = [{"domain": ".nowsecure.nl", "expiry": 1690714605, "httpOnly": True, "name": "cf_clearance", "path": "/", "sameSite": "None", "secure": True, "value": "IOt5_jFk89BojBTV0NWAPj8zh4xq_zSxxt.2scnbY.4-1659175005-0-150"}]