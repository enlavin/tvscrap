import re
from storm.locals import *
import config

class Show(object):
    __storm_table__ = 'shows'
    id = Int(primary=True)
    name = Unicode()
    regexp_filter = Unicode()
    min_size = Float()
    max_size = Float()

    def __unicode__(self):
        return self.name

    def match(self, s):
        rx = re.compile(self.regexp_filter)
        return rx.match(s)

class Episode(object):
    __storm_table__ = 'episodes'
    id = Int(primary=True)
    show_id = Int()
    show = Reference(show_id, Show.id)
    name = Unicode() # SxxEyy
    filename = Unicode()
    torrent = Unicode()
    size = Float()
    queued = Bool()
    downloaded = Bool()

    def __unicode__(self):
        return self.name

class Config(object):
    __storm_table__ = 'config'
    id = Int(primary=True)
    varname = Unicode()
    value = Unicode()

    def __unicode__(self):
        return self.varname

import sys
import os.path
def get_program_folder():
    pass

def get_db_filename():
    return "tvscrap.db" # FIXME!
    try:
        if len(config.DB) > 0 and config.DB[0] == '/':
            pass
    except AttributeError:
        return os.path.join(get_program_folder(), "tvscrap.db")

def connect_db():
    dsn = "sqlite:%s" % get_db_filename()
    return create_database(dsn)

