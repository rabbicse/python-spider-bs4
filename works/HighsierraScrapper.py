from bs4 import BeautifulSoup
import urllib
from logs.LogManager import LogManager
from spiders.Spider import Spider
from utils.Regex import Regex
from utils.Utils import Utils

__author__ = 'rabbi'


class HighsierraScrapper():
    def __init__(self, url):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.url = url

    def scrapData(self):
        try:
            host = ('Host', 'shop.highsierra.com')
            data1 = self.spider.fetchData(self.url, host=host)
            data = self.spider.fetchData(self.url, host=host)
            if data:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)
                asin_chunk = soup.find('optgroup', {'label': 'Available Items'})
                if asin_chunk:
                    asins = asin_chunk.find_all('option')
                    if asins and len(asins) > 0:
                        all_image_link = self.regex.getSearchedData('(?i)var changeSwatchSecureURL = "([^"]*)"', data)
                        print all_image_link
                        if all_image_link:
                            for asin in asins:
                                image_link = all_image_link
                                if asin and asin.get('value'):
                                    image_link = image_link + '&ASIN=' + asin.get('value') + '&zoomType=pan'
                                    print image_link
                                    self.scrapImages(image_link)

        except Exception, x:
            print x

    def scrapImages(self, image_url):
        try:
            data = self.spider.fetchData(image_url)
            if data:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                data = self.regex.reduceNbsp(data)
                soup = BeautifulSoup(data)
                print soup.prettify(encoding='utf-8')
                original_image_div = soup.find_all('div', class_='javascriptEnabled')
                if original_image_div:
                    images = original_image_div.find_all('img')
                    for image in images:
                        print image

        except Exception, x:
            print x
