def fibb(num):
    n = 2
    fibl = [1, 1]
    
    for i in range(num):

        pfib = fibl[n-1]
        ppfib = fibl[n-2]
        
        fibl.append(pfib + ppfib)

        n += 1

    return fibl
