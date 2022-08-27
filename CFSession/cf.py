import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
import time
import sys
import json
import json

STDOUT = False
DEBUG = False
DUMMY = False

def de_print(text):
    if DEBUG:
        print(text)
    
def norm_print(text):
    if STDOUT or DEBUG:
        print(text)

class CFBypass:
    def __init__(self, driver, directory) -> None:
        self.TARGET_NAME = ["Just a moment...","Please Wait..."]
        self.driver = driver
        self.directory = directory
    
    def start(self):
        return self._main_process()

    def _main_process(self):
        timeout = 0
        while any(ext in self.driver.title for ext in self.TARGET_NAME):
            timeout += 1
            if timeout >= 40:
                break
            norm_print("Waiting for cloudflare...")
            time.sleep(1)
        else:
            de_print(self.driver.title)
            de_print("Done")
            self.save_cookie_verified()
            return True
        return False

    def save_cookie_verified(self):
        de_print('saving cookie')
        json.dump(self.driver.execute_script("return navigator.userAgent;"), open(self.directory.session_path(),"w"))
        if DEBUG and DUMMY:
            de_print("DUMMY COOKIE")
            dummy = [{"domain": ".nowsecure.nl", "expiry": 1690714605, "httpOnly": True, "name": "cf_clearance", "path": "/", "sameSite": "None", "secure": True, "value": "IOt5_jFk89BojBTV0NWAPj8zh4xq_zSxxt.2scnbY.4-1659175005-0-150"}]
            json.dump(dummy , open(self.directory.cookie_path(),"w"))
        else:
            json.dump(self.driver.get_cookies() , open(self.directory.cookie_path(),"w"))
            de_print("Cookies Saved")

class SiteBrowserProcess:
    def __init__(self, destination: str, directory: str) -> None:
        self.destination = destination
        self.directory = directory
        self.process_done = False
        self.isheadless = False
        self.exception = None
        self.has_started = False
        Path(self.directory.cache_path()).mkdir(parents=True, exist_ok=True) 

    def close(self):
        try:
            self.driver.quit()
            self.proc_done = True
            sys.exit()
        except AttributeError:
            raise AttributeError("Driver has not initialized")

    def create_directory(self):
        Path(self.destination).mkdir(parents=True, exist_ok=True)

    def initialize_chromedriver(self):
        options= uc.ChromeOptions() 
        options.use_chromium=True
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        self.driver =  uc.Chrome(desired_capabilities=caps,options=options)
        self.driver.minimize_window()
        # driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"})
        norm_print("Driver initialized")
        

    def load_cf(self):
        self.driver.get(self.destination) 
        de_print(self.driver.title)
        cloud = CFBypass(self.driver, self.directory)
        return cloud.start()

    def main(self):
        self.initialize_chromedriver()
        return self.load_cf()
        

    def start(self):
        return self.main()
            
