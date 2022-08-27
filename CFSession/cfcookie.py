"""
CFSession.cfcookie
~~~~~~~~~~~~~
This module contains cookie related objects/functions for cfSession
"""

from .cfdirmodel import cfDirectory
from .cfbrowser import cfSession
import pickle
import os

class cfCookieHandler: 
    def __init__(self,name):
        self.name = name

    def dump(self,session: cfSession, directory: str = None):
        "Dumps session cookies"
        directory = os.path.join(session.directory.cache_path(), self.name)
        pickle.dump(session.session.cookies, open(directory, "wb"))

    def load(self,session: cfSession, directory: str = None):
        "Loads cookies to session"
        directory = os.path.join(session.directory.cache_path() ,self.name)
        session.session.cookies.update(pickle.load(open(directory, "rb")))




