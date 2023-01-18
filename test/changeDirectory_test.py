from CFSession import cfDirectory
from CFSession import cfSession
import os
if __name__ == "__main__":
    session = cfSession(directory=cfDirectory("customdirectory",chromedriver_path=os.path.join(os.path.dirname(__file__), "bin/chromedriver108.exe")))
    res = session.get("https://nowsecure.nl") #A Cloudflare protected site
    print(res.content)
