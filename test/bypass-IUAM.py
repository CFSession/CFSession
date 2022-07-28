import CFSession

if __name__ == "__main__":
    session = CFSession.cfSession()
    res = session.post("https://nowsecure.nl/") #A Cloudflare protected site
    print(res.content)

