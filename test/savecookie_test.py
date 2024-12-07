from CFSession import cfSession
from CFSession import cfCookieHandler
from CFSession import cfDirectory
import os

if __name__ == "__main__":
    session = cfSession()
    res = session.get("https://secure.kinuseka.us") #IUAM protected site
    cookies = cfCookieHandler("nowsecure.json") #Filename
    cookies.dump(session)
