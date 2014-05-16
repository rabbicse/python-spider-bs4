import getopt
import sys
from works.EbagsScrapper import EbagsScrapper
from works.PentaTransaction import PentaTransaction
from works.TrggroupScrapper import TrggroupScrapper
from works.WalgreensScrapper import WalgreensScrapper

__author__ = 'Rabbi'


class Main:
    def __init__(self):
        pass

    def runSpider(self, argv):
        try:
            opts, args = getopt.getopt(argv, 'hs:', ['help', 'spider='])
        except Exception, x:
            print x
            self.usage()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                self.usage()
                sys.exit()
            elif opt in ('-s', '--spider'):
                self.startScrapper(arg)

    def startScrapper(self, arg):
        if arg == 'ebags':
            self.scrapEbags()
        elif arg == 'trggroup':
            self.scrapTrggroup()
        elif arg == 'pentatr':
            self.scrapPentaTransaction()
        elif arg == 'walgreens':
            self.scrapWalgreens()
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


if __name__ == "__main__":
    main = Main()
    main.runSpider(sys.argv[1:])

