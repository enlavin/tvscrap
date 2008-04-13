# -*- coding: utf-8 -*-
"""
torrents.py

Inyecta un torrent en el programa por defecto para
iniciar su desacarga.
"""
import urllib
import os
import sys
import config

class TorrentManager(object):
    """ Descarga un torrent y se lo pasa al cliente por defecto """
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.full_filename = os.path.join(config.TORRENT_DIR, self.filename)

    def _download_torrent(self):
        """ Descarga un .torrent en un fichero """
        ftorrent = file(self.full_filename, "wb+")
        urltorrent = urllib.urlopen(self.url)
        ftorrent.write(urltorrent.read())
        ftorrent.close()

    def __call__(self):
        self._download_torrent()
        print self.full_filename
        if sys.platform != 'win32':
            # TODO: hacer una funcion que hable con mldonkey
            # sin depender de un script externo
            # external helper
            result = os.system("tvscrap_helper.sh \"%s\"" % self.full_filename)
            return result == 0
        else:
            # default windows torrent handler
            import win32api
            win32api.ShellExecute(0, "open",
                    self.full_filename, "", config.TORRENT_DIR, 0)
            return True

