# -*- coding: utf-8 -*-
"""
db.py

Modelos de la BD de series
"""
# GNU General Public Licence (GPL)
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
import os
import re
import sqlite3
import sys
import six


class TVConfigError(Exception):
    """
    Excepcion de configuracion incorrecta de la
    BD de series
    """
    pass


@six.python_2_unicode_compatible
class Show(object):
    """model for a tv show"""

    def __init__(self, id, name, regexp_filter, min_size, max_size):
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
        self.size = size
        self.queued = queued
        self.downloaded = downloaded

    def __str__(self):
        return u"%s, %s" % (self.show.name, self.name)

    def urls(self):
        return self.url.split("\n")

#Show.episodes = st.ReferenceSet(Show.id, Episode.show_id)


class Config(object):
    """ Modelo para manejar configuracion del programa """
    __storm_table__ = 'config'
    #varname = st.Unicode(primary=True)
    #value = st.Unicode()

    def __unicode__(self):
        return self.varname


def config_program_folder():
    """
    Fabrica el nombre de la BD de series a partir
    del directorio HOME en Win32 y POSIX
    """
    if sys.platform == 'win32':
        homedir = "%s%s" % \
                (os.environ.get("HOMEDRIVE"), os.environ.get("HOMEPATH"))
    else:
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
    """ Devuelve el nombre de la BD de series """
    homedir = config_program_folder()
    return os.path.join(homedir, "tvscrap.db")


class DB(object):
    def __init__(self):
        self.conn = sqlite3.connect(get_db_filename())

    def all_the_shows(self):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT id, name, regexp_filter, min_size, max_size
                FROM shows
                ORDER BY name""")
            for row in c:
                yield Show(*row)
        finally:
            c.close()

    def find_episode_by_number(self, show_name, episode_number):
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT episodes.id, episodes.show_id, episodes.name, episodes.url, episodes.filename, episodes.torrent, episodes.size, episodes.queued, episodes.downloaded
                      FROM episodes, shows
                      WHERE shows.name = ? AND shows.id = episodes.show_id AND episodes.name = ?
                      ORDER BY episodes.name""", (show_name, episode_number))
            row = c.fetchone()
            if row is None:
                return None
            return Episode(show_name, *row)
        finally:
            c.close()

    def save_episode(self, episode):
        c = self.conn.cursor()
        try:
            c.execute("""
                INSERT INTO episodes
                      SELECT episodes.id, episodes.show_id, episodes.name, episodes.url, episodes.filename, episodes.torrent, episodes.size, episodes.queued, episodes.downloaded
                      VALUES ()
                      FROM episodes, shows
                      WHERE shows.name = ? AND shows.id = episodes.show_id AND episodes.name = ?
                      ORDER BY episodes.name""", (show_name, episode_number))
            # TODO: update the ID
            if row is None:
                return None
        finally:
            c.close()


def connect_db():
    """ Conecta con la BD de series """
    return DB()

