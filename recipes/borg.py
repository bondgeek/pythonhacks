'''
adapted from:
*http://code.activestate.com/recipes/66531/

with clarifications from:
*http://snippets.dzone.com/posts/show/651
'''


class Singleton(object):
    '''There will only instance of this class, or subclass'''
    def __new__(cls):
        if not '_instance' in cls.__dict__:
            cls._instance = object.__new__(cls)
        return cls._instance

class Borg(object):
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state


class MyBorg(Borg):
    '''a simple Borg that lets you set attributes using key words'''
    def __init__(self, **kwargs):
        Borg.__init__(self)
        for key in kwargs:
            setattr(self, key, kwargs[key])
        self._keys = kwargs.keys()


my = MyBorg(a = 1)
my = MyBorg(b = 1)

print("\nJust one my: a=%s b=%s, id: %d" % 
    (my.a, my.b, id(my)))

my2 = MyBorg(one = 'a')
my2 = MyBorg(two = 'b')

print("\nmy2 is different: one=%s two=%s, id: %d" % 
    (my2.one, my2.two, id(my2)))


print("my2 has my's attributes--hasattr(my2, 'a'): %s" %
      hasattr(my2, 'a'))

class Today(Singleton):
    def __init__(self):
        from datetime import date
        self.date = date.today()
    def __repr__(self):
        return str(self.date)

today = Today()
ajourdhui = Today()

print("\nSingleton has only one instance.")
print("values: %s %s  ids: %d %d" % 
      (today, ajourdhui, id(today), id(ajourdhui)))
