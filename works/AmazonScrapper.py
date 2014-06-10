from bs4 import BeautifulSoup
import os
from logs.LogManager import LogManager
from spiders.Spider import Spider
from utils.Csv import Csv
from utils.Regex import Regex
from utils.Utils import Utils

__author__ = 'rabbi'


class AmazonScrapper():
    def __init__(self, url):
        self.logger = LogManager(__name__)
        self.spider = Spider()
        self.regex = Regex()
        self.utils = Utils()
        self.url = url
        self.base_product_url = 'http://www.amazon.com/dp/'
        self.base_image_url = 'http://ecx.images-amazon.com/images/I/'
        self.csvWriter = Csv('amazon.csv')
        csvDataHeader = ['URL', 'HTML Path', 'Image URLS']
        self.csvWriter.writeCsvRow(csvDataHeader)

    def scrapData(self):
        try:
            host = ('Host', 'www.amazon.com')
            data = self.spider.fetchData(self.url, host=host)
            if data:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                searchParams = self.regex.getSearchedData('(?i)var searchParams = {([^\}]*)}', data)
                searchParams = searchParams.split(',')
                seller = ''
                marketPlaceId = ''
                useMYI = ''
                for searchParam in searchParams:
                    searchParam = self.regex.reduceBlankSpace(searchParam)
                    searchParam = self.regex.replaceData('\'', '', searchParam)

                    if searchParam.startswith('seller'):
                        seller = searchParam.split(':')[1].strip()
                        seller = seller.decode('string-escape')
                    if searchParam.startswith('marketplaceID'):
                        marketPlaceId = searchParam.split(':')[1].strip()
                        marketPlaceId = marketPlaceId.decode('string-escape')
                    if searchParam.startswith('useMYI'):
                        useMYI = searchParam.split(':')[1].strip()
                        useMYI = useMYI.decode('string-escape')
                params = {'seller': seller,
                          'marketPlaceId': marketPlaceId,
                          'useMYI': useMYI}
                ajax_url = 'http://www.amazon.com/gp/aag/ajax/productWidget.html'
                self.scrapAjaxPage(ajax_url, params, host)
        except Exception, x:
            print x

    def scrapAjaxPage(self, url, params, host):
        try:
            data = self.spider.fetchData(url, host=host, parameters=params)
            if data:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                productList = self.regex.getSearchedData('var AAGProductWidgetAsinList = new Array\(([^\)]*)\)', data)
                products = productList.split(',')
                for productId in products:
                    productId = productId.replace('"', '')
                    product_url = self.base_product_url + productId
                    self.scrapProductDetails(product_url, productId)
        except Exception, x:
            print x

    def scrapProductDetails(self, url, productId):
        try:
            data = self.spider.fetchData(url)
            if data:
                dl_path = './html/%s.html' % productId
                if self.downloadHtml(dl_path, data):
                    data = self.regex.reduceNewLine(data)
                    data = self.regex.reduceBlankSpace(data)
                    soup = BeautifulSoup(data)
                    image_chunk = soup.find('div', id='imageBlock_feature_div')
                    if image_chunk:
                        image_urls = []
                        images = image_chunk.find_all('img', {'alt': ''})
                        for image in images:
                            image_url = str(image.get('src'))
                            image_url_extension = image_url.split('/')[-1]
                            image_url_extension = self.regex.replaceData('(?i)_[a-zA-Z]+\d+_', '_SL2560_', image_url_extension)
                            image_urls.append(self.base_image_url + image_url_extension)
                        csvData = [url, dl_path, ', '.join(image_urls)]
                        print csvData
                        self.csvWriter.writeCsvRow(csvData)
        except Exception, x:
            print x

    def downloadHtml(self, downloadPath, text):
        try:
            directory = os.path.dirname(downloadPath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            dl_file = open(downloadPath, 'wb')
            dl_file.write(text)
            return True
        except Exception, x:
            print x
        return False