from utils.Csv import Csv

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
        self.csvWriter = Csv('trggroup.csv')
        csvDataHeader = ['Name1', 'Name2', 'Dimension1', 'Dimension2', 'Spec1', 'Spec2', 'Spec3', 'Product Details',
                         'Image']
        self.csvWriter.writeCsvRow(csvDataHeader)
        self.proxy = urllib2.ProxyHandler({'http': '184.168.55.226:80'})

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
            loginData = self.spider.login(self.loginUrl, loginCredentials, proxy=self.proxy)
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

            name1 = ''
            name2 = ''
            spec1 = ''
            spec2 = ''
            ch1 = ''
            ch2 = ''
            ch3 = ''
            ch4 = ''
            ch5 = ''
            ch6 = ''
            productDetail = ''
            if self.regex.isFoundPattern(
                    '(?i)<table width="100%">\s*<tr>\s*<td style="font-size:13px;" class="bold">.*?</td>\s*</tr>\s*</table>',
                    data):
                nameChunk = self.regex.getSearchedData(
                    '(?i)(<table width="100%">\s*<tr>\s*<td style="font-size:13px;" class="bold">.*?</td>\s*</tr>\s*</table>)',
                    data)
                nameChunks = self.regex.getSearchedDataGroups(
                    '(?i)<td style="font-size:13px;" class="bold">([^<]*)</td>\s*</tr>\s*<tr>\s*<td>([^<]*)</td></tr>',
                    nameChunk)
                name1 = nameChunks.group(1)
                name2 = nameChunks.group(2)
                specChunks = self.regex.getSearchedDataGroups('<tr><td>([^<]*)<br>([^<]*)</td>', nameChunk)
                spec1 = nameChunks.group(1)
                spec2 = nameChunks.group(2)

            if self.regex.isFoundPattern('(?i)<table width="100%">\s*<tr style="font-weight:bold;">.*?</tr>\s*</table>',
                                         data):
                characteristics = self.regex.getSearchedData(
                    '(?i)(<table width="100%">\s*<tr style="font-weight:bold;">.*?</tr>\s*</table>)',
                    data)
                soup = BeautifulSoup(characteristics)
                chs = soup.find_all('td')
                ch1 = chs[0].text
                ch2 = chs[1].text
                ch3 = chs[2].text
                ch4 = chs[3].text
                ch5 = chs[4].text
                ch6 = chs[5].text

            if self.regex.isFoundPattern('(?i)<div style="overflow:auto;width:100%;height:\d+px;">.*?</div>', data):
                detailsChunk = self.regex.getSearchedData(
                    '(?i)(<div style="overflow:auto;width:100%;height:\d+px;">.*?</div>)', data)
                soup = BeautifulSoup(detailsChunk)
                productDetail = soup.find('div').text.strip()

            imageSrc = self.regex.getSearchedData('(?i)</td><td align="center"><a target="_blank" href="([^"]*)"', data)
            imageUrl = 'http://www.trggroup.net/victorinox/' + imageSrc
            imageName = self.regex.getSearchedData('(?i)([a-zA-Z0-9\.]+)$', imageSrc)
            csvData = [name1, name2, spec1, spec2, ch1 + ': ' + ch4, ch2 + ': ' + ch5, ch3 + ': ' + ch6, productDetail,
                       imageName]
            print csvData
            self.csvWriter.writeCsvRow(csvData)
            print 'Downloading image from URL: ', imageUrl
            self.spider.downloadFile(imageUrl, './images/' + imageName, self.proxy)



