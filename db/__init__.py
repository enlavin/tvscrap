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

from db import queries


class TVConfigError(Exception):
    """
    Excepcion de configuracion incorrecta de la
    BD de series
    """
    pass


def config_program_folder():
    """
    Fabrica el nombre de la BD de series a partir
    del directorio HOME en Win32 y POSIX
    """
    if sys.platform == 'win32':
        homedir = "{}{}".format(
            os.environ.get("HOMEDRIVE"), os.environ.get("HOMEPATH"))
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
    """name of the configuration sqlite file"""
    homedir = config_program_folder()
    return os.path.join(homedir, "tvscrap.db")


def connect_db():
    conn = sqlite3.connect(get_db_filename())
    return queries.Queries(conn)
