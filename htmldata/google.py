import urllib2
import re

from datetime import date
from BeautifulSoup import BeautifulSoup

"""
Google Finance History,
Thanks to:  http://code.activestate.com/recipes/576495/

"""

gmonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

gtoday = date.today()
googlefinance = "http://www.google.com/finance"

def tolinkdate(dt):
    '''python date to date used in link, e.g. startdate=Apr+25%2C+2000'''
    mstr = gmonths[dt.month-1]
    
    return "%s+%s%%2C+%s" % (mstr, dt.day, dt.year)

def fromgdate(datestr, refdate=None):
    '''dd-Mmm-yy to python date'''
    def getmonth(mstr):
        m_ = [n+1 for n in range(len(gmonths)) 
              if gmonths[n].upper()==mstr.upper()]
        return m_[0] if m_ else None
    
    if not refdate:
        refdate = date.today()
    refyear = refdate.year % 100
 
    dd, mmm, yy = datestr.split('-')
    mm = getmonth(mmm)
    if not mm:
        return None

    yy = int(yy)
    refcentury = 100 * (refdate.year // 100)
    refcentury += 0 if yy <= refyear else -1
    yy += refcentury

    return date(yy, mm, int(dd)) 

def get_finance_page(value):
    link = googlefinance + "?q=%s"%value

    page = urllib2.urlopen(link).read()
    return page

def get_history_link(page, daterange=None):

    findhistorical = re.findall('/historical\?q.*\"', page)

    histlink = findhistorical[0].replace('\"', '')
    
    datestr = ''
    if daterange:
        datestr = '&startdate=%s&enddate=%s' % (tolinkdate(daterange[0]),
                                                tolinkdate(daterange[1]))

    return googlefinance + histlink + datestr
    
def get_history_csv(link):
    csvlink = link + '&output=csv'
    return urllib2.urlopen(csvlink).read()

def get_history(ticker, begdate=None):    
    '''Given ticker returns array of historical google finance data.
       OHLC + Volume for each date
    
    '''
                
    def datarow(rowx):
        rowdata = rowx.split(',')
        try:
            dt = fromgdate(rowdata[0])
        except:
            print("date problem: %s " %  rowdata)
            return None
    
        try:
            ohlcv = map(float, rowdata[1:])
        except:
            print("map problem: %s" % rowdata[1:])
            return None
    
        rvalue = [dt]
        rvalue.extend(ohlcv)
        return rvalue
        
    daterange = None
    if begdate:
        daterange = (begdate, date.today())
    
    page_ = get_finance_page("MUB")
    histlink = get_history_link(page_, daterange)
    print("Hist Link:  %s" % histlink)

    csvdata = get_history_csv(histlink).split('\n')

    return [datarow(row) for row in csvdata[1:] if row]    

if __name__ == "__main__":

    csv = get_history("MUB", date(2006,12,31))

