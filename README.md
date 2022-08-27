# CFSession
A python script utilizing undetected-chromedriver to collect session cookies in a cloudflare IUAM protected site


## How it works
It relies on a modified selenium (undetected-chromedriver) to cloak on sites that block selenium based sessions. 
When a program is able to pass through the IAUM or Captcha verification the program immedietely saves the session token to cache to be able to access to the site right away without needing to verify again when program closes(until the token expires).

The library wraps around requests library.

**Tested request types:**
* GET
* POST

**Untested request types: but functionally implemented:**
* PUT
* PATCH
* DELETE

## Usage:

**Normal Usage:**

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



## Installation:
`python3 -m pip install CFSession`

**or**

`pip3 install CFSession`








## Question: 

**Why not just scrape fully on selenium?** There are some use cases that selenium might potentially cause more workloads than using requests directly, as selenium is a programmable browser, the output as well are dynamic and often not consistent. This does not say that `requests` does not apply to this problem. There are also some uses like, **IUAM** sites completely blocks `requests` library and your program is heavily written soley for `requests` then this might be for you.



**Is this just a requests wrapper?** not fully. I havent implemented the entire `requests` functions and will probably will not be adding until I have certain understanding on how they work. So I rely on people accessing the 'deep level' code that I have intentionally kept open incase there are some specific use cases

for example you can directly access the `requests.Session` object directly in the `cfSession` object
```py
from CFSession import cfSession

cfs = cfSession()
cfs.session #<--- A requests.Session object
```

## Disclaimer:
This library was created with the sole purpose of educational purposes only, any rules/laws/ToS broken should only be held at the sole responsibility of the user.

