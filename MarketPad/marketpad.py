
import bgpy.QL as ql

import bgpy.xl.xl_markets as xlmm
reload(xlmm)

import alprion.structures.scales as scales
reload(scales)

from bgpy.bgpyXL import isColumn, rowIfColumn

from bgpy.bgpyXL import xlDate
from bgpy.xl.xl_markets import addPortfolioBond, addTermStructure
from bgpy.xl.xl_markets import toPrice, toYield, oasCalc, bondVol

from alprion.structures import MarketFile
from alprion.structures.scales import GovtCurve, Scale
from alprion.structures.volatility import VolCurve
from alprion.structures.modelcurve import ModelScale

# can go in alprion.structures
class marketcurves(object):
    def __init__(self):
        self.zcrv = ql.ZCurve()
        self.bma = ql.RatioCurve(datadivisor=100.0)
        self.govt = GovtCurve()
        self.bcrv = self.govt.termstructure
        self.ussv = VolCurve(datadivisor=100.0)
        self.mmascale = Scale(call=("10Y", 100.0), datadivisor=100.0,
                          coupon="par")
        self.mmdscale = Scale(call=("10Y", 100.0), datadivisor=100.0,
                          coupon=.05)

        self.curvenames_ = ('zcrv', 'bma', 'govt', 'bcrv', 'ussv',
                            'mmascale', 'mmdscale')

    @property
    def curves_(self):
        return dict(zip(self.curvenames_,
                        tuple([getattr(self, crv, None)
                               for crv in self.curvenames_])))
        
    def update(self, curvedate, _swapsettle, _marketdata):
        """
        Update from MarketFile structure.
        
        """
        
        print("updating")
        self.curvedate = curvedate
        self.swapsettle = _swapsettle
        
        self.zcrv.from_pfile(_swapsettle, _marketdata['pfile'])
        self.bma.update(self.zcrv, _marketdata['bmaswaps'])

        self.govt.update(_marketdata['ustotr'], curvedate)
        
        self.ussv.update(_marketdata['ussv'])
        self.mmascale.update(_marketdata['mma'], curvedate)

        self.tenorlevels_ = {'zcrv': self.zcrv.tenorpar,
                'bma': self.bma.parRatio,
                'bcrv': self.bcrv.tenorpar,
                'ussv': self.ussv,
                'mma': lambda tnr: marketdata['mma'].get(tnr, " ")/100.,
                'govt': lambda tnr: self.govt.tenor(tnr)['yield']
                }
        
    def updateMMD(self, tenors, curve):
        '''
        TODO:  need to be able to create bonds without curve
        '''
        if hasattr(self, "curvedate"):
            tenors = tuple(rowIfColumn(tenors))
            curve = tuple(rowIfColumn(curve))
            _marketdata = dict(zip(tenors, curve))
            
            self.mmdscale.update(_marketdata, self.curvedate)
        
    def tenorlevels(self, tenor):
        tnr = tenor.upper()
        return dict([(crv, self.tenorlevels_[crv](tenor))
                     for crv in self.tenorlevels_])
    
    def __getitem__(self, key):
        return getattr(self, key, None)
    
    def get(self, key, defvalue=None):
        return getattr(self, key, defvalue)

    def modelCurve(self, spreaddata):
        self.modelcurve = ModelScale(self.zcrv,
                                spreaddata,
                                self.mmascale.curvedate)
        self.model = self.modelcurve.termstructure
        
        # add to directory
        self.curvenames_ += ('model',)        
        self.tenorlevels_['model'] = self.model.tenorpar

        
#define globals
tradedate = None
swapsettle = None
markets = None
marketdata = {}

def getMarkets(filename, trigger):
    global marketdata, markets
    global tradedate, settle
    
    print('\ngetMarkets')

    mkt = MarketFile(filename).read
    
    update = True 
    if marketdata:
        update = not (mkt['timestamp'] == marketdata.get('timestamp',
                                                         ' '))
        
    if update:
        marketdata = mkt

        mm, dd, yy = marketdata.get('tradedate', (None, None, None))
        tradedate = ql.toDate(dd, mm, yy)

        if not tradedate:
            tradedate = ql.Date.todaysDate()

        mm, dd, yy = marketdata.get('swapsettle', (None, None, None))
        swapsettle = ql.toDate(dd, mm, yy)
        
        if not swapsettle:
            swapsettle = ql.TARGET().advance(tradedate, 2, ql.Days)

        if not markets:
            print("initializing curves")
            markets = marketcurves()
        
        markets.update(tradedate, swapsettle, marketdata)
    
    return marketdata.get('timestamp', None)

def getTradeDate(trigger):
    return markets['curvedate'].ISO()
    
def addMMDScale(tenor, curves, trigger):
    markets.updateMMD(tenor, curves)
    return "mmdscale"
    
def getCurveElement(curvename, tenor, trigger):
    return markets.tenorlevels(tenor)[curvename]

def getCurvesForTenor(curves, tenor, trigger):
    return [getCurveElement(crv, tenor, trigger) for crv in curves]

def getMMABond(tenor, type, trigger):
    return getScaleBond('mmascale', tenor, type, trigger)

def addCurve(key, trigger):
    return addTermStructure(key, markets[key])

def valueScaleBond(scale, tenor, spread, ratio, vol,
                   refcurve,
                   fields):
    '''
    Returns specified fields from asset swap BondValue object

    If an empty value, or None is specified a standard list of attributes
    is returned:  ('bondyield', 'oasYield', 'ratio', 'spread', 'dv01')

    '''    
    refcurve = markets.curves_.get(refcurve, markets.zcrv)
    
    if not fields:
        fields =  ('bondyield', 'oasYield', 'ratio', 'spread', 'dv01')
    if not hasattr(fields, "__iter__"):
        fields = (fields, )
        
    _scale = markets.curves_.get(scale, None)
    if _scale:
        aswValue = _scale.bondValue(tenor,
                                    refcurve,
                                    spread,
                                    ratio,
                                    vol)
        if aswValue:
            return tuple([aswValue.get(a, None) for a in fields])
    return ('N/A', )

def getScaleBond(scale, tenor, type, refcurve, trigger):
    t = tenor.upper()

    mscale= markets.curves_.get(scale, None)
    refcurve = markets.curves_.get(refcurve, markets.zcrv)
    
    if not mscale:
        print("Invalid scale in getScaleBond: %s" % scale)
        return None
    
    mbond = mscale.bonds.get(t, None)
    bondyield = mscale.bondyields.get(t, None) 
    
    m_oasYield, m_ratio = None, None
    if mbond and bondyield:
        bondprice = mbond.toPrice(bondyield)
        
        assetSwap = mbond.assetSwap()
        
        if type.upper() == "R":
            val = assetSwap.solveSpread(refcurve, bondprice,
                                        baseSpread=0.0,
                                        solveRatio=True,
                                        vol=markets.ussv(t)
                                        )
            
        else:
            ratio = markets.tenorlevels(t)['bma']
            val = assetSwap.solveSpread(refcurve, bondprice,
                                        baseSpread=0.0,
                                        baseRatio=ratio,
                                        solveRatio=False,
                                        vol=markets.ussv(t)
                                        )
        
    return (val.bondyield, val.oasYield, val.ratio, val.spread, val.dv01)

def addModelCurve(tenors, spreaddata):
    global markets

    try:
        spreaddata = dict(zip(tenors, spreaddata))    
        markets.modelCurve(spreaddata)
    except:
        raise
    
    return ('model')
    
if __name__ == '__main__':
    print("\n\nRunning script....\n")
    getMarkets('pfile.close', 1)

    print("\nTest...")
    call = ql.Call(ql.toDate(1, 1, 2021), 100.0)    
    bnd = ql.SimpleBond(.05, ql.toDate(1,1,2040), callfeature=call)
    asw = bnd.assetSwap()
    
    val = asw.value(markets.govt.termstructure, vol=.16)
    
    print("  one...")
    spreaddata = {}
    for tenor in markets.mmascale.bonds:
        ratio = markets.bma.parRatio(tenor)
        bnd = ql.SimpleBond(.05, markets.mmascale.bonds[tenor].maturity,
                            callfeature = call)
        asw = bnd.assetSwap()
        yld = markets.mmascale.bondyields[tenor]
        prc = bnd.toPrice(yld)
        
        val = asw.solveSpread(markets.zcrv, prc, baseRatio=ratio, vol=markets.ussv(tenor))
        spread, ratio, vol = val.spread, val.ratio, val.vol
        
        spreaddata[tenor] = (bnd.coupon, yld, spread, ratio, vol)
    
    print("  two...")    
    mdl = ModelScale(markets.zcrv, spreaddata, markets.mmascale.curvedate)
    
    print("  three...")
    for tenor in markets.mmascale.bonds:
        bnd = ql.SimpleBond(.05, markets.mmascale.bonds[tenor].maturity,
                            callfeature = call)
        asw = bnd.assetSwap()
        prc = bnd.toPrice(markets.mmascale.bondyields[tenor])
        
        val = asw.value(mdl.termstructure, vol=mdl.volCurve(tenor))
        
        print("%4s %2.6f %2.5f %2.6f %3.3f %3.3f %2.6f" % 
             (tenor, val.bondyield, markets.mmascale.bondyields[tenor], 
             val.oasYield, val.price, val.oasPrice, val.callvalue))
        
    sprTenors = [t for t in spreaddata]
    sprValues = [spreaddata[t] for t in spreaddata]
    # rc = addModelCurve(sprTenors, sprValues)
    # print rc