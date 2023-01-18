from CFSession import cfSession
from CFSession import cfCookieHandler
from CFSession import cfDirectory

if __name__ == "__main__":
    session = cfSession(cfDirectory(chromedriver_path="./bin/chomedriver108"))
    res = session.get("http://nowsecure.nl") #IUAM protected site
    cookies = cfCookieHandler("nowsecure.json") #Filename
    cookies.dump(session)