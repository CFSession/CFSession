from CFSession import cfSession
from CFSession import cfDirectory

if __name__ == "__main__":
    session = cfSession(cfDirectory(chromedriver_path="./bin/chomedriver108"))
    res = session.post("https://nowsecure.nl") #Method Not Allowed
    res.raise_for_status()