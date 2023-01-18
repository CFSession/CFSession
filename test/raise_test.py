from CFSession import cfSession


if __name__ == "__main__":
    session = cfSession(version_main=108)
    res = session.post("https://nowsecure.nl") #Method Not Allowed
    res.raise_for_status()