import getopt
import sys
from works.AmazonScrapper import AmazonScrapper
from works.EbagsScrapper import EbagsScrapper
from works.HighsierraScrapper import HighsierraScrapper
from works.PentaTransaction import PentaTransaction
from works.TrggroupScrapper import TrggroupScrapper
from works.WalgreensScrapper import WalgreensScrapper

__author__ = 'Rabbi'


class Main:
    def __init__(self):
        pass

    def runSpider(self, argv):
        spider = ''
        url = ''
        try:
            opts, args = getopt.getopt(argv, 'hs:u:', ['help', 'spider=', 'url='])
        except Exception, x:
            print x
            self.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.usage()
                sys.exit()
            elif opt in ('-s', '--spider'):
                spider = arg
            elif opt in ('-u', '--url'):
                url = arg

        self.startScrapper(spider, url)

    def startScrapper(self, arg, url=None):
        if arg == 'ebags':
            self.scrapEbags()
        elif arg == 'trggroup':
            self.scrapTrggroup()
        elif arg == 'pentatr':
            self.scrapPentaTransaction()
        elif arg == 'walgreens':
            self.scrapWalgreens()
        elif arg == 'highsierra':
            self.scrapHighsierra(url)
        elif arg == 'amazon':
            self.scrapAmazon(url)
        else:
            print 'Unknown spider type.'
            self.usage()

    def usage(self):
        print 'Usage: '
        print '\nTo run spider write: python -s spidername or python --spider spidername'
        print '\nExample:'
        print '\nTo run Ebags spider write: python -s ebags'
        print '\nTo run Trggroup spider write: python -s trggroup'

    def scrapEbags(self):
        print 'Running spider for Ebags...'
        scrapper = EbagsScrapper()
        scrapper.scrapData()

    def scrapTrggroup(self):
        print 'Running spider for Trggroup...'
        scrapper = TrggroupScrapper()
        scrapper.scrapData()

    def scrapPentaTransaction(self):
        print 'Running spider for Penta transaction...'
        scrapper = PentaTransaction()
        scrapper.scrapData()

    def scrapWalgreens(self):
        print 'Running spider for Walgreens...'
        scrapper = WalgreensScrapper()
        scrapper.scrapData()

    def scrapHighsierra(self, url):
        print 'Running spider for Highsierra...'
        scrapper = HighsierraScrapper(url)
        scrapper.scrapData()

    def scrapAmazon(self, url):
        print 'Running spider for Amazon...'
        scrapper = AmazonScrapper(url)
        scrapper.scrapData()


if __name__ == "__main__":
    main = Main()
    main.runSpider(sys.argv[1:])

