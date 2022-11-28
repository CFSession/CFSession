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
      >>> defaults.dcp = DesirecCapabilities().CHROME #You can modify DesiredCapabilites
      >>> CFSession.cf.SiteBrowserProcess(ignore_defaults=True,defaults=defaults)
    """
    def __init__(self) -> None:
        self.options = uc.ChromeOptions() 
        self.dcp = DesiredCapabilities().CHROME 
    def options_default(self) -> uc.ChromeOptions():    
        self.options.use_chromium=True
        self.options.add_argument("--disable-renderer-backgrounding")
        self.options.add_argument("--disable-backgrounding-occluded-windows")
        return self.options

    def desired_capabilites_default(self) -> DesiredCapabilities:
        self.dcp["pageLoadStrategy"] = "eager"
        return self.dcp
