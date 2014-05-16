import os
from logs.LogManager import LogManager
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup

__author__ = 'Rabbi'


class PentaTransaction():
    def __init__(self):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.loginUrl = 'http://www.v4.penta-transaction.com/telematica_v4/login_ing.jsp'
        self.username = 'web9501201'
        self.password = '784693'
        self.collectionUrl = 'http://www.trggroup.net/victorinox/index.php?p=124'
        self.mainUrl = 'http://www.penta-transaction.com'

    def scrapData(self):
        self.onLogin()
        data = self.spider.fetchData(self.mainUrl)
        if data and len(data) > 0:
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            print data

    def onLogin(self):
        '''
        Credentials are:
        action	login_access
        i
        p
        password	sdfsdf
        username	sdfsdf
        '''
        try:
            print self.loginUrl
            loginCredentials = {'username': self.username,
                                'password': self.password}
            loginData = self.spider.login(self.loginUrl, loginCredentials)
            if loginData and len(loginData) > 0:
                loginData = self.regex.reduceNewLine(loginData)
                loginData = self.regex.reduceBlankSpace(loginData)
                print 'Login: '
                print loginData
        except Exception, x:
            print 'There was an error when login'
        return False