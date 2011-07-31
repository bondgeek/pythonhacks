'''
A simple spread sheet gadget
'''

  
class SpreadSheet(object):
    _cells = {}
    tools = {}
    def __setitem__(self, key, formula):
        if not isinstance(key, str):
            raise ValueError, "SpreadSheet key must be a string"
        if not isinstance(formula, str):
            formula = str(formula)
        self._cells[key] = formula
    def getformula(self, key):
        return self._cells[key]
    def show(self):
        for key in self._cells:
            print key, self._cells[key]
    def __getitem__(self, key ):
        try:
            rvalue = eval(self._cells[key], self.tools, self)
        except KeyError:
            rvalue = self.tools.get(key, None)
        return rvalue


