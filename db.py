from storm.locals import *

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
    queued = Boolean()
    downloaded = Boolean()


