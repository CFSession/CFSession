from CFSession import cfSession
from CFSession import cfCookieHandler

if __name__ == "__main__":
    session = cfSession()
    res = session.get("http://nowsecure.nl") #IUAM protected site
    cookies = cfCookieHandler("nowsecure.json") #Filename
    cookies.dump(session)