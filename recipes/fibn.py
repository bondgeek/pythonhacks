def fibn(num=0):
    fibs = [1,1]
    if num < 3:
        return fibs[:num]
    else:
        for n in range(1,num):
            fibs.append(fibs[n]+fibs[n-1])
        return fibs
