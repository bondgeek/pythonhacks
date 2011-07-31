class mydict(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

    def __getitem__(self, key):
        print "hi!"
        return self.get(key, None)
