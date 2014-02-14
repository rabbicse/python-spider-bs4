__author__ = 'Rabbi'

import urllib2
from logs.LogManager import LogManager
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup


class TrggroupScrapper():
    def __init__(self):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.loginUrl = 'http://www.trggroup.net/victorinox/index.php'
        self.username = 'Cespanosa@luggageNmore.com'
        self.password = '@#5M0k137'
        self.collectionUrl = 'http://www.trggroup.net/victorinox/index.php?p=124'
        self.mainUrl = 'http://www.trggroup.net/victorinox/'
        self.url = 'http://www.ebags.com/brands'

    def scrapData(self):
        if self.onLogin() is True:
            print 'Successfully logged in.'
            data = self.spider.fetchData(self.collectionUrl)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)
                allCollections = soup.find('table', class_='sidebar').find_all('td', class_='sidebara')
                if allCollections and len(allCollections) > 0:
                    print 'Total collection found: ' + str(len(allCollections))
                    for collection in allCollections:
                        collectionUrl = collection.get('onclick')
                        collectionUrl = self.regex.getSearchedData('(?i)location.href=\'([^\']*)\'', collectionUrl)
                        collectionUrl = self.mainUrl + collectionUrl
                        print collectionUrl
                        self.scrapCollectionData(collectionUrl)

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
            loginCredentials = {'action': 'login_access',
                                'i': '',
                                'p': '',
                                'username': self.username,
                                'password': self.password}
            proxy = urllib2.ProxyHandler({'http': '64.34.14.28'})
            loginData = self.spider.login(self.loginUrl, loginCredentials, proxy=proxy)
            if loginData and len(loginData) > 0:
                loginData = self.regex.reduceNewLine(loginData)
                loginData = self.regex.reduceBlankSpace(loginData)
                soup = BeautifulSoup(loginData)
                if soup.find('input', {'value': 'Search'}):
                    return True
        except Exception, x:
            print 'There was an error when login'
        return False

    def scrapCollectionData(self, url):
        data = self.spider.fetchData(url)
        if data and len(data) > 0:
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            soup = BeautifulSoup(data)
            products = soup.find('table', class_='tblProducts').find_all('a')
            if products and len(products) > 0:
                for product in products:
                    self.scrapProductData(self.mainUrl + product.get('href'))

    def scrapProductData(self, url):
        print 'Product URL: ', url
        data = self.spider.fetchData(url)
        if data and len(data) > 0:
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            soup = BeautifulSoup(data)



