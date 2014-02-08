import re
import time
from logs.LogManager import LogManager
from utils.Csv import Csv
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup

__author__ = 'Rabbi'


class EbagsScrapper():
    def __init__(self):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.mainUrl = 'http://www.ebags.com'
        self.url = 'http://www.ebags.com/brands'

    def scrapData(self):
        data = self.spider.fetchData(self.url)
        if data and len(data) > 0:
            allBrandLinks = []
            soup = BeautifulSoup(data)
            brandChunks = soup.find_all('div', class_='brandList4Col')
            if brandChunks and len(brandChunks) > 0:
                for brandChunk in brandChunks:
                    brandLinks = brandChunk.find_all('a')
                    if brandLinks and len(brandLinks) > 0:
                        for brandLink in brandLinks:
                            brandUrl = brandLink.get('href')
                            print brandUrl
                            allBrandLinks.append(self.mainUrl + brandUrl)

            print allBrandLinks
            for brandUrl in allBrandLinks:
                self.scrapBrandData(brandUrl)
                break

    def scrapBrandData(self, url):
        print 'Brand URL: ' + url
        data = self.spider.fetchData(url)
        if data and len(data) > 0:
            soup = BeautifulSoup(data)
            productLinks = soup.find_all('div', class_='itemProductName')
            if productLinks and len(productLinks) > 0:
                for productLink in productLinks:
                    productUrl = productLink.find('a').get('href')
                    print self.mainUrl + productUrl

    def scrapProductDetail(self, url):
        data = self.spider.fetchData(url)