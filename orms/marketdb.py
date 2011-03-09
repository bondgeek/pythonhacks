from autumn import Model, autumn_db, OneToMany, ForeignKey
    
from alprion import AlprionCfg_, PathJoin, DATADIR

dbcfg = AlprionCfg_.read('database', ("marketdb"))
autumn_db.conn.connect('sqlite3', PathJoin(DATADIR, dbcfg['marketdb']))
        
class Instruments(Model):
    class Meta:
        defaults = {'name': 'xxx',
                    'source': 'unkown'}
        
    
class Series(Model):
    class Meta:
        defaults = {'label': 'close'}

  
class Timeseries(Model):
    '''sqlite3: marketdb.db timeseries
        
    '''
    instrument = ForeignKey('Instruments')
    
