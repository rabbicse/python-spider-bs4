import os
from logs.LogManager import LogManager
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
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            allBrandLinks = []
            soup = BeautifulSoup(data)
            brandChunks = soup.find_all('div', class_='brandList4Col')
            if brandChunks and len(brandChunks) > 0:
                for brandChunk in brandChunks:
                    brandLinks = brandChunk.find_all('a')
                    if brandLinks and len(brandLinks) > 0:
                        for brandLink in brandLinks:
                            brandUrl = brandLink.get('href')
                            allBrandLinks.append(self.mainUrl + brandUrl)

            print 'Total brands found: ', str(len(allBrandLinks))
            for brandUrl in allBrandLinks:
                self.scrapBrandData(brandUrl)

    def scrapBrandData(self, url, page=1):
        brandUrl = url if page is 1 else url + '?page=' + str(page)
        print 'Brand URL: ', brandUrl
        data = self.spider.fetchData(brandUrl)
        if data and len(data) > 0:
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            soup = BeautifulSoup(data)
            productLinks = soup.find_all('div', class_='itemProductName')
            if productLinks and len(productLinks) > 0:
                for productLink in productLinks:
                    productUrl = productLink.find('a').get('href')
                    productDetailUrl = self.mainUrl + productUrl
                    print 'Product detail url: ', productDetailUrl
                    fileName = self.regex.getSearchedData('(?i)^.*?(\d+)$', productUrl) + '.html'
                    print 'File Name: ', fileName
                    self.scrapProductDetail(self.mainUrl + productUrl, fileName)

            ## Check if any next page
            if soup.find('a', class_='pagingNext') is not None:
                nextLink = soup.find('a', class_='pagingNext').get('href')
                print nextLink
                if nextLink is not None and len(nextLink) > 0:
                    print 'Pagination found...'
                    return self.scrapBrandData(url, page + 1)

    def scrapProductDetail(self, url, filename):
        data = self.spider.fetchData(url)
        if data and len(data) > 0:
            data = self.regex.reduceNewLine(data)
            data = self.regex.reduceBlankSpace(data)
            directory = os.path.dirname('./products/' + filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            print 'File saving path: ', os.path.abspath('./products/' + filename)
            dl_file = open('./products/' + filename, 'wb')
            dl_file.write(data)
            dl_file.close()
