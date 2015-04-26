# -*- coding: utf-8 -*-
import re
import six


@six.python_2_unicode_compatible
class Show(object):
    """model for a tv show"""

    def __init__(self, id=None, name=None, regexp_filter=None, min_size=None, max_size=None):
        self.id = id
        self.name = name
        self.regexp_filter = regexp_filter
        self.min_size = min_size
        self.max_size = max_size

    def __str__(self):
        return self.name

    def match(self, candidate, relax=False):
        """ Comprueba si el parametro cumple la expresion regular """

        if re.compile(self.regexp_filter).match(candidate) is not None:
            return True

        # try a more relaxed version of the regexp, just for the fun of it
        if relax:
            relaxed_regexp = self.regexp_filter.replace(r'\s', r'[\s_.-]')
            if re.compile(relaxed_regexp).match(candidate) is not None:
                return True

        return False

    def check_size(self, size):
        """ Comprueba si el tamaño está dentro de los límites """
        return (self.max_size == 0.0 or size <= self.max_size) and \
            (self.min_size == 0.0 or size >= self.min_size)


@six.python_2_unicode_compatible
class Episode(object):
    """model for an episode"""

    def __init__(self, show_name, id, show_id, name, url, filename, torrent, size, queued, downloaded):
        self.id = id
        self.show_id = show_id
        self.show_name = show_name
        self.name = name
        self.url = url
        self.filename = filename
        self.torrent = torrent
        self.size = float(size)
        self.queued = int(queued) != 0
        self.downloaded = int(downloaded) != 0

    def __str__(self):
        return u"%s, %s" % (self.show.name, self.name)

    def urls(self):
        return self.url.split("\n")


@six.python_2_unicode_compatible
class Config(object):
    """model for the configuration variables"""

    def __init__(self, varname, value):
        self.varname = varname
        self.value = value

    def __str__(self):
        return self.varname


