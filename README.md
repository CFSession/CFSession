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
V1.3.0 now supports a much more easier way of modifying chromeoptions
```py
from CFSession import Options, cfSession
import undetected_chromedriver as uc

options = Options()
options.chrome_options = uc.ChromeOptions()
session = cfSession(options=options)

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

