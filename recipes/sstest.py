from bondgeekdb import instrumentsdb
from bondgeek.utils.cusiputils import validate_cusip
from bondgeek.gadgets.spreadsheet import SpreadSheet
ss = SpreadSheet(tools = {'cusip': validate_cusip})
ss['cusip1'] = '000416k7'
ss['cusip2'] = 'len(cusip1)'
ss['cusip3'] = 'cusip(cusip1)'
ss.show()
