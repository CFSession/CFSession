"""
CFSession.cf
~~~~~~~~~~~~~
This module contains the internal operations for controlling the behavior of the chromedriver
"""
#uc
import undetected_chromedriver as uc
from seleniumwire import undetected_chromedriver as ucwire
#Sel
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Modules
from .cfmodels import cfDirectory, Options
from .cfdefaults import Required_defaults, cfConstant
from pathlib import Path
import typing
import time
import sys
import json
import threading
from loguru import logger
_de_log = logger.bind(name="CFSession")

#Not a constant. CAPITAL for more readable syntax
#If constant is ever declared we will use CONST_VARIABLE_NAME
IGNORE_WARN = True
STDOUT = False
DEBUG = False
DUMMY = False

def de_print(text: str):
    if DEBUG:
        try:
            _de_log.debug(text)
        except UnicodeEncodeError:
            _de_log.error("Uni Err, ascii md")
            _de_log.debug(text.encode('ascii', 'ignore'))
        except Exception as e:
            _de_log.exception("[warn] Error occured on a debugger de", e)
    
    
def norm_print(text: str):
    if STDOUT or DEBUG:
        try:
            _de_log.info(text)
        except UnicodeEncodeError:
            _de_log.error("Uni Err, ascii md")
            _de_log.info(text.encode('ascii', 'ignore'))
        except Exception as e:
            _de_log.exception("[warn] Error occured on a debugger norm", e)

def warn_print(text, level: int = 2): # 0-Important, 1-If possible, 2-Unimportant (debug purposes)
    acceptable = STDOUT + DEBUG
    if IGNORE_WARN and not DEBUG:
        return
    elif level == 0:
        print(f"[WARN] {text}")
        print("-"*20)
        print("You received this warning as it might be critical to the processs of the program")
        print*("Ignore this warning by using CFSession.cf.IGNORE_WARN = True")
    elif level <= acceptable:
        print(f"[WARN] {text}")

class CFBypass:
    def __init__(self, driver: uc.Chrome, directory, target = cfConstant.DEF_CLOUDFLARE_TARGET, timeout: int = 40, bypass_mode: bool = True) -> None:
        self.TARGET_NAME = target
        self.driver = driver
        self.website = driver.current_url
        self.directory: cfDirectory = directory
        self.timeout = timeout
        self.bypass_mode = bypass_mode
        self.children = []
        self.switching = [0, -1]
    
    def start(self):
        return self._main_process()
    
    def find_element(self, element, max_attempts=3, target: uc.Chrome =False):
        attempt = 1
        while True:
            de_print(f"Finding element: {element}")
            try:
                if target:
                    target.find_element(*element)
                return self.driver.find_element(*element)
            except StaleElementReferenceException as e:
                de_print(f"Error element stale {attempt}/{max_attempts} {e}")
                if attempt == max_attempts:
                    raise
                time.sleep(1)
                attempt += 1

    def WaitForElement(self, time_to_sleep, time_to_wait = 10):
        WebDriverWait(self.driver, time_to_wait).until(
            EC.visibility_of(
            self.find_element(
            (By.TAG_NAME, 'body'),
        )))
        time.sleep(time_to_sleep)
    
    def window_manager(self):
        if len(self.driver.window_handles) > 2:
            oldest_window = self.driver.window_handles[0]
            self.driver.switch_to.window(oldest_window)
            self.driver.close()
            self.window_handles = self.driver.window_handles
            self.driver.switch_to.window(self.window_handles[-1])  # Switch to the latest window

    def init_bypass(self):
        self.driver.execute_script(f'window.open("{self.website}","_blank");')
        self.WaitForElement(3)
        self.driver.switch_to.window(window_name=self.driver.window_handles[0]) 
        self.WaitForElement(3)
        self.driver.close()
        self.driver.switch_to.window(window_name=self.driver.window_handles[0])
    
    def click_bypass(self):
        #https://stackoverflow.com/questions/76575298/how-to-click-on-verify-you-are-human-checkbox-challenge-by-cloudflare-using-se
        try:
            self.driver.switch_to.window(window_name=self.driver.window_handles[0])
            self.WaitForElement(2)
            WebDriverWait(self.driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()
            time.sleep(1)
            de_print("Clicked on verify")
            self.driver.switch_to.window(window_name=self.driver.window_handles[-1])
            self.driver.execute_script(f'window.open("{self.website}","_blank");')
            time.sleep(7)
        except TimeoutException:
            de_print("Click bypass Timeout")
        except Exception:
            warn_print("An error occured on click_bypass")
        self.driver.switch_to.window(window_name=self.driver.window_handles[self.switching[0]])
        self.switching.reverse()

    def main_bypass(self):
        self.click_bypass()

    def scan_windows(self):
        norm_print('Scanning windows')
        for window_handle in self.driver.window_handles:
            self.driver.switch_to.window(window_handle)
            title = self.driver.title
            de_print(f"cur: {title}")
            if not any(ext in title for ext in self.TARGET_NAME):
                return True

    def _main_process(self):
        if self.bypass_mode:
            self.init_bypass()
            return self._main_process_bypass()
        return self._main_process_non_bypass()
    
    def _main_process_bypass(self):
        for _ in range(self.timeout):
            self.main_bypass()
            if self.scan_windows():
                de_print(f'Final: {self.driver.title}')
                de_print("Done")
                self.save_cookie_verified()
                return True
            self.window_manager()
            norm_print("Waiting for cloudflare...")
            time.sleep(1)
        de_print("Failed to bypass, returning failure")
        return False

    def _main_process_non_bypass(self):
        for _ in range(self.timeout):
            if self.scan_windows():
                de_print(f'Final: {self.driver.title}')
                de_print("Done")
                self.save_cookie_verified()
                return True
            norm_print("Waiting for site...")
            time.sleep(1)
        de_print("Timeout reached, returning failure")
        return False

    def save_cookie(self, cookies, file):
        """Cookie save, requires driver cookies and file"""
        json.dump(cookies, file)
    
    def save_agent(self, agent, file):
        """UserAgent save, requires agent and file"""
        json.dump(agent, file)
        
    def save_cookie_verified(self):
        de_print('saving cookie')
        self.save_agent(self.driver.execute_script("return navigator.userAgent;"), open(self.directory.session_path(),"w"))
        if DEBUG and DUMMY:
            de_print("DUMMY COOKIE")
            dummy = cfConstant.DEBUG_DUMMY
            self.save_cookie(dummy , open(self.directory.cookie_path(),"w"))
        else:
            self.save_cookie(self.driver.get_cookies(), open(self.directory.cookie_path(),"w"))
            de_print("Cookies Saved")
    
    def clear_children(self):
        for child in self.children:
            child.join()

class SiteBrowserProcess:
    def __init__(self, destination: str, directory: cfDirectory, options: Options, headless_mode: bool = False, process_timeout: int = 10, bypass_mode: bool = True, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.ignore_defaults = options.ignore_defaults
        self.destination = destination
        self.directory = directory
        self.process_done = False
        self.isheadless = headless_mode
        self.bypass_mode = bypass_mode
        self.exception = None
        self.has_started = False
        self.p_timeout = process_timeout
        self.userOptions = options
        Path(self.directory.cache_path()).mkdir(parents=True, exist_ok=True) 

    def close(self):
        "Quits driver gracefully"
        try:
            #close remaining windows
            self.driver.quit()
            self.proc_done = True
        except AttributeError:
            de_print("Close attempt but self.driver is not found")

    def create_directory(self):
        Path(self.destination).mkdir(parents=True, exist_ok=True)
    
    def _init_chromedriver(self, *args, **kwargs):
        "Generates new Chromedriver, with chromeoptions checking"
        try:
            options = self.userOptions.chrome_options
            desired_cap = self.userOptions.desired_capabilities
            cdriver_path = self.directory.chromedriver_path()
            if self.userOptions.proxy:
                driver = ucwire.Chrome(desired_capabilities=desired_cap,options=options,driver_executable_path=cdriver_path,headless=self.isheadless,seleniumwire_options=self.userOptions.get_seleniumwire_options(),*args, **kwargs)
            else:
                driver = uc.Chrome(desired_capabilities=desired_cap,options=options,driver_executable_path=cdriver_path,headless=self.isheadless,*args, **kwargs)
        except RuntimeError:
            if self.ignore_defaults:
                warn_print("userOptions for dcp and chromeoptions is reset but kept the attributes",0)
            self.userOptions.reset_dcp(defaults=(not self.ignore_defaults))
            self.userOptions.reset_chromeoptions(defaults=(not self.ignore_defaults))
            options = self.userOptions.chrome_options
            desired_cap = self.userOptions.desired_capabilities
            cdriver_path = self.directory.chromedriver_path()
            if self.userOptions.proxy:
                driver = ucwire.Chrome(desired_capabilities=desired_cap,options=options,driver_executable_path=cdriver_path,headless=self.isheadless,seleniumwire_options=self.userOptions.get_seleniumwire_options(),*args, **kwargs)
            else:
                driver = uc.Chrome(desired_capabilities=desired_cap,options=options,driver_executable_path=cdriver_path,headless=self.isheadless,*args, **kwargs)
        return driver

    def initialize_headless(self) -> str:
        headless_driver = self._init_chromedriver(*self.args, **self.kwargs)
        de_print("Headless mode driver initialized")
        user_agent = headless_driver.execute_script("return navigator.userAgent;").replace("Headless", "")
        de_print("Collected userAgent: %s" % user_agent)
        headless_driver.quit()
        return user_agent
    
    def initialize_chromedriver(self):
        """Main initialzor for SBP"""
        if self.isheadless:
            norm_print("Headless Mode detected")
            user_agent = self.initialize_headless()
            self.userOptions.user_agent = user_agent
            #Post headless reset to prevent checking
            self.userOptions.reset_dcp(defaults=(not self.ignore_defaults))
            self.userOptions.reset_chromeoptions(defaults=(not self.ignore_defaults))
        self.driver =self._init_chromedriver(*self.args, **self.kwargs)
        norm_print("Driver initialized")
        
    def init_cf(self,CFobj: CFBypass = CFBypass) -> CFBypass:
        de_print(f"Bypass mode enabled: {self.bypass_mode}")
        return CFobj(self.driver, self.directory, timeout = self.p_timeout, bypass_mode = self.bypass_mode)

    def load_cf(self):
        self.driver.get(self.destination) 
        de_print(self.driver.title)
        cloud = self.init_cf()
        return cloud.start()

    def main(self):
        self.initialize_chromedriver()
        try:
            self.driver.minimize_window()
        except WebDriverException as e:
            warn_print("Failed to minimize window.",level=1)
            de_print(e)
        return self.load_cf()

    def start(self):
        return self.main()
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()