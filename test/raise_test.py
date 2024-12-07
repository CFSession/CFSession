from CFSession import cfSession
from CFSession import cfDirectory
import os

if __name__ == "__main__":
    session = cfSession()
    res = session.post("https://secure.kinuseka.us/notfound") #Method Not Allowed
    res.raise_for_status()
