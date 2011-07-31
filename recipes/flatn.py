def flatn(obj, levels=None, _ltypes = (list, tuple), _counter=0):

    if isinstance(obj, _ltypes):
        objtype = type(obj)

        if not levels or _counter < levels:
            _counter += 1
        
            objl = []
            for n in obj:
                objl.extend(flatn(n, 
                                  levels=levels, _counter=_counter))
        else:
            objl = list(obj)

        return objtype(objl)
    else:
        return [obj]


