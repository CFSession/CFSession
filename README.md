# CFSession
A python script utilizing undetected-chromedriver to collect session cookies in a cloudflare IUAM protected site


## How it works
It relies on a modified selenium (undetected-chromedriver) to cloak on sites that block selenium based sessions. 
When a program is able to pass through the IAUM or Captcha verification the program immedietely saves the session token to cache to be able to access to the site without needing to verify again (until the token expires).

The program then uses requests library to collect scraped data using the saved token.

**Currently supported request types:**
* GET
* POST

## Usage:

```py
import CFSession

if __name__ == "__main__":
    session = CFSession.cfSession()
    res = session.get("https://nowsecure.nl/")
    print(res.content)
```








## Question: 

**Why not just scrape fully on selenium?** selenium is great, able to scrape. However there are some use cases that using `selenium` is a total waste of resource power and is REALLY slow to initialize especially when performance and running time matters. It takes 3-5 seconds for `selenium` to start up before you can even begin scraping which is 40x SLOWER than just using `requests`.



**Is this just a requests wrapper?** not fully. I havent implemented the entire `requests` functions and will probably will not be adding until I have certain understanding on how they work. So I rely on people accessing the 'deep level' code that I have intentionally kept open incase there are some specific use cases

for example you can directly access the `requests.Session` object directly in my `cfSession` object
```py
from CFSession import cfSession

cfs = cfSession()
cfs.session() #<--- A requests.Session object
```

