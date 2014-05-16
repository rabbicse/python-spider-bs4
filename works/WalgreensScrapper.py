__author__ = 'rabbi'
import os
from logs.LogManager import LogManager
from utils.Utils import Utils
from spiders.Spider import Spider
from utils.Regex import Regex
from bs4 import BeautifulSoup

class WalgreensScrapper():
    def __init__(self):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.url = 'http://www.walgreens.com/store/catalog/shopLanding'

    def scrapData(self):
        data = self.spider.fetchData(self.url)
        if data and len(data) > 0:
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            print data
            allBrandLinks = []
            soup = BeautifulSoup(data)