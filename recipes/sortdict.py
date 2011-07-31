class SortDict(dict):
    def __init__(self, input=None, default=None):
        dict.__init__(self, input)
        self.default = default

    def key_sort(self, reverse=False):
        ksort =  self.keys()
        ksort.sort(reverse=False)

        return ksort

    def __missing__(self):
        return self.default



