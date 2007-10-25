class Show(object):
    __storm_table__ = 'serie'
    id = Int(primary=True)
    name = Unicode()
    regexp_filter = Unicode()
    min_size = Int()
    max_size = Int()

class Episode(object):
    __storm_table__ = 'episode'
    id = Int(primary=True)
    show_id = Int()
    name = Unicode() # SxxEyy
    torrent = Unicode()
    size = Int()
    queued = Boolean()
    downloaded = Boolean()


