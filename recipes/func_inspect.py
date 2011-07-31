import inspect

def fundoc(func):
    '''intropect basic function info'''

    try:    
        #(args, varargs, varkw, defaults)
        argspec = inspect.getargspec(func)

    except TypeError:
        return None

    if argspec[3]:
        dflt = len(argspec[3])
        for n in range(len(argspec[0])-1, 
                       len(argspec[0])-len(argspec[3])-1, 
                       -1):
            argspec[0][n] = "=".join((argspec[0][n], 
                                      str(argspec[3][dflt-1])))
            dflt -= 1

    f_signature = ", ".join(argspec[0])

    if argspec[1]:
        f_signature = ", ".join((f_signature,
                                 "".join(("*", argspec[1]))))
    
    if argspec[2]:
        f_signature = ", ".join((f_signature,
                                 "".join(("**", argspec[2]))))
    
    f_signature = f_signature.join(("(",")"))
    f_signature = "".join([func.func_name, f_signature])

    return f_signature 
