from CFSession import cfDirectory
from CFSession import cfSession
import os
if __name__ == "__main__":
    session = cfSession(directory=cfDirectory('./artificialDirectory'),version_main=114)
    res = session.get("https://nowsecure.nl") #A Cloudflare protected site
    print(res.content)
