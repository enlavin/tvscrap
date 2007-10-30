from storm.locals import *
import config

class Show(object):
    __storm_table__ = 'shows'
    id = Int(primary=True)
    name = Unicode()
    regexp_filter = Unicode()
    min_size = Int()
    max_size = Int()

class Episode(object):
    __storm_table__ = 'episodes'
    id = Int(primary=True)
    show_id = Int()
    name = Unicode() # SxxEyy
    filename = Unicode()
    torrent = Unicode()
    size = Int()
    queued = Bool()
    downloaded = Bool()

class Config(object):
    __storm_table__ = 'config'
    id = Int(primary=True)
    varname = Unicode()
    value = Unicode()

import sys
import os.path
def get_program_folder():
    pass

def get_db_filename():
    try:
        if len(config.DB) > 0 and config.DB[0] == '/':
            pass
    except AttributeError:
        return os.path.join(get_program_folder(), "tvscrap.db")

def connect():

    dsn = "sqlite:%s" % dbpath
