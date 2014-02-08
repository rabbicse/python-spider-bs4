from cStringIO import StringIO
from logs.LogManager import LogManager
from spiders import config
import gc
import time

__author__ = 'Rabbi'

import urllib
import urllib2
import cookielib
import gzip


class Spider:
    def __init__(self):
        self.logger = LogManager(__name__)
        self.opener = None
        self.mycookie = None

    def login(self, url, loginInfo, retry=0):
        """
        Login request for user
        url = '' Ex. http://www.example.com/login
        loginInfo = {} Ex. {'user': 'user', 'pass': 'pass'}
        """
        host = ('Host', 'www.amazon.com')
        conn = ('Connection', 'keep-alive')
        enc = ('Accept-Encoding', 'gzip, deflate')
        ac = ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        ln = ('Accept-Language', 'en-us,en;q=0.5')
        self.opener = self.createOpener([config.USER_AGENT, conn, enc, ac, ln, host], self.createCookieJarHandler())
        urllib2.install_opener(self.opener)
        try:
            return self.opener.open(url, urllib.urlencode(loginInfo)).read()
        except Exception, x:
            self.logger.error(x.message)
            if retry < config.RETRY_COUNT:
                self.login(url, loginInfo, retry + 1)
        return None

    def fetchData(self, url, parameters=None, retry=0):
        """
        Fetch data from a url
        url='' Ex. http://www.example.com, https://www.example.com
        parameters={} Ex. {'user': 'user', 'pass': 'pass'}
        """
        conn = ('Connection', 'keep-alive')
        enc = ('Accept-Encoding', 'gzip, deflate')
        ac = ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        ln = ('Accept-Language', 'en-us,en;q=0.5')

        myheaders = [config.USER_AGENT, conn, ac, ln, enc]
        if self.opener is None:
            self.opener = self.createOpener(myheaders)
            urllib2.install_opener(self.opener)
        try:
            if parameters is None:
                response = self.opener.open(url, timeout=config.TIMEOUT)
                self.mycookie = response.headers.get('Set-Cookie')
                buf = StringIO(response.read())
                data2 = gzip.GzipFile('', 'r', 0, buf).read()
                response.close()
                del response
                gc.collect()
                del gc.garbage[:]
                gc.collect()
                return data2
            else:
                response = self.opener.open(url, urllib.urlencode(parameters), timeout=config.TIMEOUT)
                if response is not None:
                    data = response.read()
                    response.close()
                    del response
                    gc.collect()
                    del gc.garbage[:]
                    gc.collect()
                    return data
                else:
                    if retry < config.RETRY_COUNT:
                        time.sleep(5)
                        self.fetchData(url, parameters, retry + 1)
        except Exception, x:
            print x
            self.logger.debug(x)
            if retry < config.RETRY_COUNT:
                time.sleep(5)
                self.fetchData(url, parameters, retry + 1)
        return None

    def createOpener(self, headers=None, handler=None):
        """
        Create opener for fetching data.
        headers = [] Ex. User-agent etc like, [('User-Agent', HEADERS), ....]
        handler = object Ex. Handler like cookie_jar, auth handler etc.
        return opener
        """
        opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),
                                      urllib2.HTTPHandler(debuglevel=0),
                                      urllib2.HTTPSHandler(debuglevel=0))
        if headers is not None:
        #            print headers
            opener.addheaders = headers
        if handler is not None:
            opener.add_handler(handler)
        return opener

    def createCookieJarHandler(self):
        """
        Create cookie jar handler. used when keep cookie at login.
        """
        cookieJar = cookielib.LWPCookieJar()
        return urllib2.HTTPCookieProcessor(cookieJar)