# -*- coding: utf-8 -*-
"""
config.py

Configuración básica editable por el usuario
"""

import sys
if sys.platform == 'win32':
    DB = "tvscrap.db"
    TORRENT_DIR = r'c:\temp'
else:
    DB = "tvscrap.db"
    TORRENT_DIR = r'/home/migue/download/torrents'

