from CFSession import cfSession
from CFSession import cfCookieHandler
from CFSession import cfDirectory
import os

if __name__ == "__main__":
    session = cfSession(chromedriver_path=os.path.join(os.path.dirname(__file__), "bin/chromedriver108"))
    res = session.get("http://nowsecure.nl") #IUAM protected site
    cookies = cfCookieHandler("nowsecure.json") #Filename
    cookies.dump(session)