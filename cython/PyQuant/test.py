import quantlib.cashflow as cf; import quantlib.time.date as d
ll = ((100., d.Date(1, 11, 2020)),)

print("testing...")
x = cf.SimpleLeg(ll)
