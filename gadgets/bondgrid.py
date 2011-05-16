#!/usr/bin/env python
'''
create a grid to allow a cusip entry, database lookup and calc
'''

import wx
import wx.grid

from bgpy.cusips import validate_cusip
from sandbox.pythonmod.gadgets.spreadsheet import SpreadSheet

class BondTable(SpreadSheet):
    def __init__(self):
        tools = {'cusip': validate_cusip}
        SpreadSheet.__init__(self, tools = tools)
    
    
class BondGridTable(wx.grid.PyGridTableBase):
    
    def __init__(self):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = { (0,0): 'cusip' 
                     }
        
        self.numbonds = 1
        
        self.rowLabels = []
        
        self.colLabels = ['Cusip', 'Description']
        
        for n in range(self.numbonds*2):
            if not n % 2:
                self.rowLabels.append(" ".join(["Bond",str(n//2+1)]))
            else:
                self.rowLabels.append("")
                
        print self.colLabels
        print self.rowLabels
        
        
    def GetNumberCols(self):
        return 2
    
    def GetNumberRows(self):
        return self.numbonds * 2
    
    def IsEmptyCell(self, row, col):
        return self.data.get((row, col)) is not None
    
    def GetValue(self, row, col):
        return self.data.get((row, col))
    
    def GetColLabelValue(self, col):
        return self.colLabels[col]
    
    def GetRowLabelValue(self, row):
        return self.rowLabels[row]
    
    def SetValue(self, row, col, value):
        pass
        
class BondGrid(wx.Frame):
    '''Frame class for bonds'''
    
    def __init__(self, parent=None, id=-1, title=None, 
                 pos=wx.DefaultPosition):
        wx.Frame.__init__(self, parent, id, title, pos,
                          size=(500,200))
        
        grid = wx.grid.Grid(self)
        
        table = BondGridTable()
        grid.SetTable(table, True)
       
        grid.SetColSize(1, 240)
        


class BondApp(wx.App):
    
    def OnInit(self):
        self.frame = BondGrid(parent=None, title="BondApp")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
def bond_app():
    app = BondApp(False)
    app.MainLoop()
    
    
if __name__ == "__main__":
    bond_app()