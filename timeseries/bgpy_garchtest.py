import numpy as np

from bgpy.math.garch import GARCH


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    import sys; sys.path.append("/Users/bartmosley/sandbox")
    import bgpy.xldb as xl
    from bgpy import PathJoin

    from alprion import DATADIR
    
    from scipy.linalg import cholesky

    
    # data files
    spx_file = PathJoin(DATADIR, "Benchmarks", "AllocationStudy.xls")
    spxdaily = xl.XLdb(spx_file, startrow=9, sheet_index=0)
    
    dow_file = PathJoin(DATADIR, "Benchmarks", "dow.xls")
    dowdaily = xl.XLdb(dow_file, sheet_index=0)
    
    # index values
    if 'spx' not in vars():
        spx = [(dt, spxdaily[dt]['SPX']) for dt in spxdaily.refcolumn
                  if spxdaily[dt]['SPX']]
              
        dow = [(dt, dowdaily[dt]['Dow']) for dt in dowdaily.refcolumn
                  if dowdaily[dt]['Dow']]
              
    # returns vector
    retseries = [np.log(dow[n][1]/dow[n-1][1]) for n in range(1, len(dow))]

    dow_d = dict(dow)
    idx_series = {'spx': [], 'dow': []}
    for n in range(1, len(spx)):
        dt, spxidx = spx[n]
        if dt in dow_d:
            dowidx = dow_d[dt]
            idx_series['spx'].append((dt, spxidx))     
            idx_series['dow'].append((dt, dowidx))
    
    print("creating return series")
    idx_returns = {'spx': [], 'dow': []}
    for k in ['spx', 'dow']:
        idx = idx_series[k]
        idx_returns[k] = [np.log(idx[n][1]/idx[n-1][1]) 
                        for n in range(1, len(idx))]
                            
    print("covariance matrix")
    CovMtx = np.cov(idx_returns['spx'], idx_returns['dow'])
    
    C = cholesky(CovMtx)
    
    print("garch variance estimates")
    g = GARCH()
    
    g(retseries, [0., .5, .5])
    
    