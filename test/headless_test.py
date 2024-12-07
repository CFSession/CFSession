from CFSession import cf
from CFSession import cfSession
import os

cf.DEBUG = True

if __name__ == "__main__": 
    session = cfSession(headless_mode=True)
    res = session.get("https://secure.kinuseka.us") #A Cloudflare protected site
    print(res.content)

    #Context Manager
    with cfSession() as session:
        res = session.get("https://secure.kinuseka.us")
        print(res.content)

