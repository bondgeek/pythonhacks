'''
A simple spread sheet gadget
'''

import re

_formula_regex = re.compile("([=+-/@])(.+)")

class SpreadSheet(object):
    '''A simple spreadsheet gadget'''
    def __init__(self, name=None, tools=None):
        self.name = name
        if tools:
            self.tools = tools
        else:
            self.tools = {}
        self._cells = {}
        
    def __setitem__(self, key, content):
        if not isinstance(key, str):
            raise ValueError, "SpreadSheet key must be a string"
        if not isinstance(content, str):
            content = str(content)
        else:
            m = re.match(_formula_regex, content)
            if m:
                content = m.group(2)
            else:
                content = """%s""" % content
        self._cells[key] = content
        
    def __getitem__(self, key ):
        try:
            rvalue = eval(self._cells[key], self.tools, self._cells)
        except KeyError:
            rvalue = self.tools.get(key, None)
        except SyntaxError:
            rvalue = str(self._cells[key])
        return rvalue
    
    def get_cell(self, key):
        return (key, self._cells[key], self[key])
    
    def show(self, keys=None):
        if not keys:
            keys = self._cells.keys()
        for key in keys:
            cell = self.get_cell(key)
            if cell:
                print("key: %s content: %s value: %s" % cell)
            else:
                print("key:  empty")


class Model(object):
    _cells = {}
    _tools = {}
    def __init__(self, name=None, tools = None):
        self.name = name
        if tools:
            _tools.update(tools)
    
    def __setitem__(self,key, content):
        if not isinstance(key, str):
            raise ValueError, "SpreadSheet key must be a string"
        self._cells[key] = ModelCell(content)
        
    def __getitem__(self, key ):
        try:
            rvalue = eval(self._cells[key], self.tools, self._cells)
        except KeyError:
            rvalue = self.tools.get(key, None)
        except SyntaxError:
            rvalue = str(self._cells[key])
        except:
            rvalue = "##Error"
        return rvalue
        
    def get_cell(self, key):
        return (key, self._cells[key], self[key])
    
    def show(self, keys=None):
        if not keys:
            keys = self._cells.keys()
        for key in keys:
            cell = self.get_cell(key)
            if cell:
                print("key: %s content: %s value: %s" % cell)
            else:
                print("key:  empty")
        

class ModelCell(object):
    '''use properties'''
    
    def __init__(self, content):
        self._content = content
        
    def __repr__(self):
        content = self._content
        if not isinstance(content, str):
            content = str(content)
        else:
            m = re.match(_formula_regex, content)
            if m:
                content = m.group(2)
            else:
                content = """%s""" % content
        return content
