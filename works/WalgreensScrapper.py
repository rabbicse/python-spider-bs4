import re
from utils.Csv import Csv

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
        self.main_url = 'http://www.walgreens.com'
        self.url = 'http://www.walgreens.com/store/catalog/shopLanding'
        self.sitemap_xml = 'http://www.walgreens.com/sitemap.xml'
        dupCsvReader = Csv()
        self.dupCsvRows = dupCsvReader.readCsvRow('walgreens.csv')
        self.csvWriter = Csv('walgreens.csv')
        csvDataHeader = ['Product Name', 'Price', 'Description', 'Shipping', 'Ingredients', 'Image']
        if csvDataHeader not in self.dupCsvRows:
            self.csvWriter.writeCsvRow(csvDataHeader)


    def scrapData(self):
        try:
            print 'First scrapping sitemap...'
            self.scrapSiteMap()

            print 'Main URL: ' + self.url
            data = self.spider.fetchData(self.url)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)
                categoryBar = soup.find('div', class_='wid150 padrt5px padlt5px float-left')
                if categoryBar:
                    categories = categoryBar.find_all('li')
                    for category in categories:
                        category_url = self.main_url + category.a.get('href')
                        self.scrapCategory(category_url)
        except Exception, x:
            print x

    def scrapSiteMap(self):
        try:
            print 'Sitemap URL: ' + self.sitemap_xml
            data = self.spider.fetchData(self.sitemap_xml)
            if data and len(data) > 0:
                soup = BeautifulSoup(data)
                product_urls = soup.find_all('loc')
                for product_url in product_urls:
                    self.scrapProductDetails(product_url.text.strip())
        except Exception, x:
            print x

    def scrapCategory(self, url):
        try:
            print 'Category URL: ' + url
            data = self.spider.fetchData(url)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)
                links = soup.find('div', id='main').find_all('a', {'class': 'SearchLinkBold text1p08em txt13px',
                                                                   'title': re.compile('(?i)View More .*?')})
                for link in links:
                    product_link = self.main_url + link.get('href')
                    self.scrapProducts(product_link)
        except Exception, x:
            print x

    def scrapProducts(self, url):
        try:
            print 'All products URL: ' + url
            data = self.spider.fetchData(url)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)
                link_divs = soup.find_all('div', class_='product-name nopad')
                for link_div in link_divs:
                    product_url = self.main_url + link_div.find('a').get('href')
                    self.scrapProductDetails(product_url)
        except Exception, x:
            print x

    def scrapProductDetails(self, url):
        try:
            print 'Product Details URL: ' + url
            data = self.spider.fetchData(url)
            if data and len(data) > 0:
                data = self.regex.reduceNewLine(data)
                data = self.regex.reduceBlankSpace(data)
                soup = BeautifulSoup(data)

                ## Field declarations
                product_name = ''
                price = ''
                description = ''
                shipping = ''
                ingredients = ''
                image = ''

                ## Operation
                product_h1 = soup.find('h1', {'itemprop': 'name'})
                if product_h1 is not None:
                    product_name = product_h1.text.strip()
                else:
                    return
                price_span = soup.find('span', {'id': 'vpdSinglePrice'})
                if price_span is not None:
                    price = price_span.text.strip()
                description_div = soup.find('div', id='description-content')
                if description_div is not None:
                    description = description_div.text.strip()
                shipping_div = soup.find('div', id='shipping-content')
                if shipping_div is not None:
                    shipping = shipping_div.text.strip()
                ingredients_div = soup.find('div', id='ingredients-content')
                if ingredients_div:
                    ingredients = ingredients_div.text.strip()
                image_img = soup.find('img', id='main-product-image')
                if image_img is not None:
                    image = image_img.get('src')
                    image = 'http:' + image
                csvdata = [product_name, price, description, shipping, ingredients, image]
                print csvdata
                if csvdata not in self.dupCsvRows:
                    self.csvWriter.writeCsvRow(csvdata)
                    self.dupCsvRows.append(csvdata)
        except Exception, x:
            print x


if __name__ == '__main__':
    scrapper = WalgreensScrapper()
    scrapper.scrapProductDetails(
        'http://www.walgreens.com/store/c/frownies-forehead-and-between-eyes-facial-patches/ID=prod6014745-product')

