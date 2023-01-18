import CFSession
from CFSession import cfDirectory

if __name__ == "__main__": 
    session = CFSession.cfSession(cfDirectory(chromedriver_path="./bin/chomedriver108"))
    res = session.get("https://nowsecure.nl") #A Cloudflare protected site
    print(res.content)

    #Context Manager
    with CFSession.cfSession() as session:
        res = session.get("https://nowsecure.nl")
        print(res.content)

