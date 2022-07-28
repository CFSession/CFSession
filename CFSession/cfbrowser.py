from urllib import response
import requests
import os
import json
cookie_path = os.path.join(os.getcwd(),".browser","cookies.json")
session_path = os.path.join(os.getcwd(),".browser","session.json")

class cfSession():
    def __init__(self):
        self.session = requests.Session()
        self._setcookies_status = self.set_cookies()

    def get(self,url,params=None, **kwargs):
        r"""Sends a GET request.
        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("GET",url,params=params,**kwargs)
    
    def post(self,url,data=None, json=None,**kwargs):
        r"""Sends a POST request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        self.url = url
        return self.request("POST",url,data=data,json=json,**kwargs)

    def put(self, url, data=None, **kwargs):
        r"""Sends a PUT request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        self.url = url
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url,data=None, **kwargs):
        r"""Sends a PATCH request.
        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        r"""Sends a DELETE request.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        self.url = url
        return self.request("DELETE", url, **kwargs)

    def reload_token(self,site_requested,reset=False):
        cookieStatus =  SiteCFBypass.cookie_available()
        if not cookieStatus[0] or reset:
            NHS = SiteCFBypass(site_requested)
            if reset:
                SiteCFBypass.delete_cookies()
            NHS.start()
            NHS.join()
        
    def set_cookies(self):
        try:
            cookies = json.load(open(cookie_path,"r"))
            selenium_headers = json.load(open(session_path,"r"))
        except FileNotFoundError:
            return False
        self.session.headers.update({"user-agent": selenium_headers})
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
        return True

    def _handle_equalfunc(self):
        if not self._setcookies_status:
            self.reload_token(self.url)
            self.set_cookies()

    def request(self,method,url,**kwargs):
        for t in range(0,2):
            try:
                if method == "GET":
                    content = self.session.get(url, **kwargs)
                elif method == "POST":
                    content = self.session.post(url, **kwargs)
                elif method == "PATCH":
                    content = self.session.patch(url, **kwargs)
                elif method == "PUT":
                    content = self.session.put(url, **kwargs)
                elif method == "DELETE":
                    content = self.session.delete(url, **kwargs)
                content.raise_for_status()
                return content
            except requests.exceptions.HTTPError as e:
                http_code = e.response.status_code
                caught_exception = e
                if http_code == 404:
                    raise NotFound()
                elif http_code == 503:
                    #CF blocked us, update the token
                    #Recheck token
                    self.reload_token(url,reset=True)
                    self.set_cookies()
                elif http_code == 403:
                    #Different blocking method, usually its an IUAM javascript challenge but sometimes a recaptcha
                    self.reload_token(url,reset=True)
                    self.set_cookies()
            except requests.exceptions.ConnectionError as e:
                caught_exception = e
                caught_message = "There has been issues with trying to connect"
                raise NetworkError(response=e)
            except requests.exceptions.URLRequired as e:
                raise URLRequired(response=e)
            except requests.exceptions.TooManyRedirects as e:
                raise TooManyRedirects(response=e)
            except requests.exceptions.Timeout as e:
                raise TimeoutError(response=e)
        else:
            caught_code = caught_exception.response.status_code
            caught_content = caught_exception.response.content
            caught_message = "There has been issues communicating with the server"
            if caught_code == 503:
                raise CloudflareBlocked(caught_code,caught_content)
            raise HTTPError(caught_code,caught_content,caught_message)
            
    def __repr__(self):
        return "<cfSession Object>"


if __name__ == "__main__":
    from cfexception import CloudflareBlocked, HTTPError, NetworkError, NotFound, URLRequired, TooManyRedirects, Timeout, ConnectTimeout, ReadTimeout
    from cf import CFBypass, SiteCFBypass
else:
    from .cfexception import CloudflareBlocked, HTTPError, NetworkError, NotFound, URLRequired, TooManyRedirects, Timeout, ConnectTimeout, ReadTimeout
    from .cf import CFBypass, SiteCFBypass



