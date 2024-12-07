import CFSession
from CFSession import cfDirectory
import os

if __name__ == "__main__": 
    session = CFSession.cfSession()
    res = session.get("https://secure.kinuseka.us") #A Cloudflare protected site
    print(res.content)

    #Context Manager
    with CFSession.cfSession() as session:
        res = session.get("https://secure.kinuseka.us")
        print(res.content)

