def f_reload(func):
    if hasattr(func, "__module__"):
        print("reloading %s" % func.__module__)
        mod = __import__(func.__module__)
        del(func)
        return reload(mod)
    else:
        print("no __module__ for %s" %func)
        return None
