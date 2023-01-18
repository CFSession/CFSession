from CFSession import cfSimulacrum
from CFSession import cf
from threading import Thread
import time

cf.DEBUG = True

def looptill(driver):
    print("Thread started, will redirect in 5 seconds")
    time.sleep(5)
    driver.get("https://www.youtube.com/watch?v=zmWstsNBcTM")

if __name__ == "__main__":
    simSession = cfSimulacrum(version_main=108)
    
    #Manually generate cookie and break down the steps of CFSession
    #This is useful for reCaptcha bypass where it requires user intervention and cannot be done fully automatically
    print("Initializing drivers")
    browserprocess = simSession.copen("https://www.youtube.com/watch?v=fgkgL8Z6z-c") # CFSession.cf.SiteBrowserProcess
    print("Create Finder object")
    simFind = simSession.find() #returns CFSession.cf.CFBypass, this also initializes the selenium driver allowing you to change it
    redirect_thread = Thread(target=looptill,args=(browserprocess.driver,),daemon=True)
    redirect_thread.start()
    simSession.search(target_title=["RAINING IN ＴＯＫＹＯ (Lofi HipHop) - YouTube"]) #Target title is the page title where it will wait until it is false.
    #"Welcome - Login" [Welcome - Login] = True | "Success login - Profile" [Welcome - Login] = False
    #simFind.TARGET_NAME = ["RAINING IN ＴＯＫＹＯ (Lofi HipHop) - YouTube"] #Alternate way to set target title (Can be used to dyanamically change target)
    
    #If you leave the page by clicking another video, it will close the window and save the cookies
    #If you haven't noticed, this will be useful for login pages where there are anti-robot verification.

    print("Done")
    
    #If you still need to access web it is still possible.
    simSession.get("https://youtube.com")

