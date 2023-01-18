from CFSession import cfSession
from CFSession import cfDirectory
import os

if __name__ == "__main__":
    session = cfSession(cfDirectory(chromedriver_path=os.path.join(os.path.dirname(__file__), "bin/chromedriver108.exe")))
    res = session.post("https://nowsecure.nl") #Method Not Allowed
    res.raise_for_status()