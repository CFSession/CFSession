<H1 align="center"><b>CFSession</b></p></H1>
<p align="center">A python script utilizing undetected-chromedriver to collect session cookies in a cloudflare IUAM protected site</p>
<p align="center">
<a href="https://pypi.org/project/CFSession"><img src="https://github.com/Kinuseka/CFSession/actions/workflows/python-package.yml/badge.svg" alt="Build Test"></a>




## How it works
It relies on a modified selenium (undetected-chromedriver) to cloak on sites that block selenium based sessions. 
When a program is able to pass through the IUAM or Captcha verification, it immediately saves the session token to access the site using requests library.

The library wraps around requests library.

**Tested request types:**
* GET
* POST

**Untested request types: but functionally implemented:**
* PUT
* PATCH
* DELETE
* OPTIONS

## Usage:

### Normal Usage:

```py
import CFSession

if __name__ == "__main__": 
    session = CFSession.cfSession()
    res = session.get("https://nowsecure.nl") #A Cloudflare protected site
    print(res.content)

    #Context Manager
    with CFSession.cfSession() as session:
        res = session.get("https://nowsecure.nl")
        print(res.content)
```
enable headless mode:

```py
session = CFSession.cfSession(headless_mode=True)
```

### How to choose chrome version:

CFSession has `*args` and `**kwargs` which simply passes it to `uc.Chrome()`
```py
from CFSession import cfSession

if __name__ == "__main__": 
    session = cfSession(version_main=95) #pick chrome version 95
```
You can also use more options from `uc.Chrome()` and pass it from there 

### How to modify chrome options:

CFSession has `CFSession.Required_defaults()` This is a class which you can use to modify `options` and `DesiredCapabilities`, the default options are pre-configured to work with bypass capabilities and other features we incorporated so we do not recommend modifying them. (Unless you know what you are doing)
```py
from CFSession import Required_defaults, cf
from undetected_chromedriver import uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

defaults = Required_defaults()
defaults.options = uc.ChromeOptions()
defaults.dcp = DesiredCapabilities().CHROME
SBP = cf.SiteBrowserProcess(ignore_defaults=True,defaults=defaults) # Generate cf.SiteBrowserProcess 
```

**CFSession** does not fully support modifying `Required_defaults()`, but there are multiple ways to hack this limitation.

1.) Using cfSession
```py
from CFSession import Required_defaults, cf, cfSession
from undetected_chromedriver import uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#cfSession uses _class_initialize to generate its own SiteBrowserProcess
def function_hack(*args,**kwargs):
    #Do ur stuff with the options and or DesiredCapabilities here.
    defaults = Required_defaults()
    defaults.options = uc.ChromeOptions()
    defaults.dcp = DesiredCapabilities().CHROME
    SBP = cf.SiteBrowserProcess(*args,**kwargs,ignore_defaults=True,defaults=defaults) # Generate cf.SiteBrowserProcess 
    return SBP
cfSession._class_initialize = function_hack
cfSession.get(...)
```

2.) Using cfSimulacrum
```py
from CFSession import Required_defaults, cf, cfSimulacrum, cfDirectory
from undetected_chromedriver import uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#Do ur stuff with the options and or DesiredCapabilities here.
defaults = Required_defaults()
defaults.options = uc.ChromeOptions()
defaults.dcp = DesiredCapabilities().CHROME
SBP = cf.SiteBrowserProcess("https://nowsecure.nl",directory=cfDirectory(),ignore_defaults=True,defaults=defaults) # Generate cf.SiteBrowserProcess 

cfsim = cfSimulacrum()
cfsim.bypass_mode = True #cfSimulacrum has bypass_mode disabled by default, set it on
cfsim.cdriver = SBP
cfsim.find() #Run bypass
response = cfsim.get("https://nowsecure.nl")
```

## Installation:
`python3 -m pip install CFSession`

**or**

`pip3 install CFSession`


## Question: 

**Why not just scrape fully on selenium?** There are some use cases that where some applications rely on a `requests` library to scrape on websites, while selenium is sensible option to prevent javascript challenges. This library will try and bypass javascript challenges by using session cookies so you can access the site just as how you would with `requests`.

**Is this just a requests wrapper?** No, it is simply an extension of `requests` library where it tries to simplify the process of bypassing cloudflare IUAM.

You can directly access the `requests.Session` object in the `cfSession.session` attribute 
```py
from CFSession import cfSession

cfs = cfSession()
cfs.session #<--- A requests.Session object
```

## Disclaimer:
This library was created with the sole purpose of educational purposes only, any rules/laws/ToS broken should only be held at the sole responsibility of the user.

