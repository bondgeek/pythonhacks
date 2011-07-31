class ra(object):
    '''test'''
    def __init__(self, initvalue = None, name='var'):
        self.value = initvalue
        self.name = name
    
    def __get__(self, obj, objtype):
        return self.value

    def __set__(self, obj, val):
        self.value = val

    def __repr__(self):
        self.value

class MyClass(object):
    x = ra(11, "var x")

