"""
http://download.finance.yahoo.com/d/quotes.csv?s=AAPL&f=sl1d1t1c1ohgv&e=.csv

"""

import urllib2
import csv

from datetime import date

yahoofinance1 = "http://download.finance.yahoo.com/d/quotes.csv?s="
yahoofinance2 = "&f=sl1d1t1c1ohgv&e=.csv"

layout = ('ticker', 'last_trade', 'trade_date', 'trade_time', 'day_change', 
          'open', 'high', 'low', 'volume')

def ydate(mdy_str):
    "mm/dd/yyyy to date object"
    try:
        mm, dd, yyyy = map(int, mdy_str.strip('"').split('/'))
        return date(yyyy, mm, dd)
        
    except:
        return None
        
def cef_nav_ticker(tickr):
    "return nav ticker, e.g. XMUBX for MUB"
    
    try:
        return tickr.upper().join(('X', 'X'))
    except:
        return None
        
    
def get_yahoo_quote(tickr, asdict=True):
    "Return current quote for ticker"
    def str_to_float(txt):
        try:
            return float(txt)
        except:
            return txt
    try:
        link = str(tickr).upper().join((yahoofinance1, yahoofinance2))    
        page = urllib2.urlopen(link).read()
        
    except:
        return None

    rdr = csv.reader([page], skipinitialspace=True)
    quote = [r for r in rdr][0]
    
    quote = map(str_to_float, quote)
    
    return dict(zip(layout, quote)) if asdict else quote

    

if __name__ == "__main__":

    csv = get_history("MUB", date(2006,12,31))

