from CFSession import cfSession
from CFSession import cf
from CFSession import cfexception
import sys

cf.DEBUG = True

def main():
    session = cfSession()
    res = session.get("https://nowsecure.nl/2332") #404 Notfound
    try:
        res.raise_for_status()
    except cfexception.HTTPError as e:
        print(f"StatusCode: {e.response.status_code}")
        print("Pass, exception for 404 not found was passed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())
    
    

