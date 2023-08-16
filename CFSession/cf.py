#UC
import undetected_chromedriver as uc
#Sel
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Modules
from .cfdirmodel import cfDirectory
from .cfdefaults import Required_defaults, cfConstant
from pathlib import Path
import typing
import time
import sys
import json
import threading

#Not a constant. CAPITAL for more readable syntax
#If constant is ever declared we will use CONST_VARIABLE_NAME
IGNORE_WARN = True
STDOUT = False
DEBUG = False
DUMMY = False

def de_print(text: str):
    if DEBUG:
        try:
            print(text)
        except UnicodeEncodeError:
            print("Uni Err, ascii md")
            print(text.encode('ascii', 'ignore'))
        except Exception as e:
            print("[warn] Error occured on a debugger de", e)
    
    
def norm_print(text: str):
    if STDOUT or DEBUG:
        try:
            print(text)
        except UnicodeEncodeError:
            print("Uni Err, ascii md")
            print(text.encode('ascii', 'ignore'))
        except Exception as e:
            print("[warn] Error occured on a debugger norm", e)

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
    def __init__(self, driver: uc.Chrome, directory, target = ["Just a moment...","Please Wait..."], timeout: int = 40, bypass_mode: bool = True) -> None:
        self.TARGET_NAME = target
        self.driver = driver
        self.website = driver.current_url
        self.directory = directory
        self.timeout = timeout
        self.bypass_mode = bypass_mode
        self.children = []
    
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

    def WaitForElement(self, i):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(
            self.find_element(
            (By.TAG_NAME, 'body'),
        )))
        time.sleep(i)

    def init_bypass(self):
        self.driver.execute_script(f'window.open("{self.website}","_blank");')
        self.WaitForElement(10)
        self.driver.switch_to.window(window_name=self.driver.window_handles[0]) 
        self.WaitForElement(5)
        self.driver.close()
        self.driver.switch_to.window(window_name=self.driver.window_handles[0])
    
    def click_bypass(self):
        #https://stackoverflow.com/questions/76575298/how-to-click-on-verify-you-are-human-checkbox-challenge-by-cloudflare-using-se
        try:
            self.driver.execute_script(f'window.open("{self.website}","_blank");')
            self.WaitForElement(5)
            WebDriverWait(self.driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title='Widget containing a Cloudflare security challenge']")))
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label.ctp-checkbox-label"))).click()
            de_print("Clicked on verify")
        except TimeoutException:
            de_print("Click bypass Timeout")
            self.driver.close()
            self.driver.switch_to.window(window_name=self.driver.window_handles[0])
        except Exception:
            warn_print("An error occured on click_bypass")

    def main_bypass(self):
        self.click_bypass()

    def _main_process(self):
        timeout = 0
        if self.bypass_mode: self.init_bypass()
        while any(ext in self.driver.title for ext in self.TARGET_NAME):
            timeout += 1
            if timeout >= self.timeout:
                break
            if self.bypass_mode: self.main_bypass()
            norm_print("Waiting for cloudflare...")
            de_print(f"cur: {self.driver.title}")
            time.sleep(1)
        else:
            de_print(self.driver.title)
            de_print("Done")
            self.save_cookie_verified()
            return True
        de_print("Failed to bypass, return failure")
        return False

    def save_cookie(self, driver, file):
        """Cookie save, requires driver and file"""
        json.dump(driver, file)

    def save_cookie_verified(self):
        de_print('saving cookie')
        json.dump(self.driver.execute_script("return navigator.userAgent;"), open(self.directory.session_path(),"w"))
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
    def __init__(self, destination: str, directory: cfDirectory, headless_mode: bool = False, ignore_defaults: bool = False, defaults: typing.Union[Required_defaults, bool] = Required_defaults(), process_timeout: int = 10, bypass_mode: bool = True, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.defaults = defaults
        self.ignore_defaults = ignore_defaults
        self.destination = destination
        self.directory = directory
        self.process_done = False
        self.isheadless = headless_mode
        self.bypass_mode = bypass_mode
        self.exception = None
        self.has_started = False
        self.p_timeout = process_timeout
        Path(self.directory.cache_path()).mkdir(parents=True, exist_ok=True) 

    def close(self):
        try:
            self.driver.quit()
            self.proc_done = True
        except AttributeError:
            raise AttributeError("Driver has not initialized")

    def create_directory(self):
        Path(self.destination).mkdir(parents=True, exist_ok=True)

    def _init_chromedriver_manual(self):
        self.driver = uc.Chrome(*self.args, **self.kwargs)

    def initialize_chromedriver(self):
        if self.ignore_defaults and not self.defaults:
            warn_print("You are overriding default arguments without cfdefaults, these may be important to work properly.\nIt is recommended to use 'CFSession.cfdefaults.RequiredDefaults' to modify changes",1)
            return self._init_chromedriver_manual()
        options = self.defaults.options_default()
        desired_cap = self.defaults.desired_capabilites_default()
        cdriver_path = self.directory.chromedriver_path() #the function will return None(default), or a str path
        try:
            self.driver =  uc.Chrome(desired_capabilities=desired_cap,options=options,driver_executable_path=cdriver_path,headless=self.isheadless,*self.args, **self.kwargs)
        except RuntimeError: #Catch if the objects were reused
            if self.ignore_defaults:
                warn_print("Required_Defaults attributes had been reset, this is a mandatory reset to prevent Runtime error due to object duplicates.",0)
            self.defaults.reset_objects()
            options = self.defaults.options_default()
            desired_cap = self.defaults.desired_capabilites_default()
            self.driver =  uc.Chrome(desired_capabilities=desired_cap,options=options,driver_executable_path=cdriver_path,*self.args, **self.kwargs)
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
            
