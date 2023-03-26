from CFSession import cfDirectory
from CFSession import cfSession

if __name__ == "__main__":
    session = cfSession()
    res = session.get("https://nowsecure.nl") #A Cloudflare protected site
    print(res.content)
