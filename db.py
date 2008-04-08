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

    def check_size(self, size):
        return (self.max_size == 0.0 or size <= self.max_size) and \
                (self.min_size == 0.0 or size >= self.min_size)


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

Show.episodes = ReferenceSet(Show.id, Episode.show_id)

class Config(object):
    __storm_table__ = 'config'
    id = Int(primary=True)
    varname = Unicode()
    value = Unicode()

    def __unicode__(self):
        return self.varname

import sys
import os

def config_program_folder():
    homedir = os.environ.get("HOME")
    if not homedir:
        configdir = '.'
    else:
        configdir = os.path.join(homedir, ".tvscrap")

    if not os.path.exists(configdir):
        os.mkdir(configdir)
    else:
        if not os.path.isdir(configdir):
            raise TVConfigError()

    return configdir

def get_db_filename():
    homedir = config_program_folder()
    return os.path.join(homedir, "tvscrap.db")

def connect_db():
    dsn = "sqlite:%s" % get_db_filename()
    return create_database(dsn)

