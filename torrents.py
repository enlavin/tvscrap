import urllib
import tempfile
import os
import sys
import config

class TorrentManager(object):
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.full_filename = os.path.join(config.TORRENT_DIR, self.filename)

    def _download_torrent(self):
        f = file(self.full_filename, "wb+")
        u = urllib.urlopen(self.url)
        f.write(u.read())
        f.close()

    def __call__(self):
        self._download_torrent()
        print self.full_filename
        if sys.platform <> 'win32':
            # external helper
            r = os.system("tvscrap_helper.sh \"%s\"" % self.full_filename)
            return r == 0
        else:
            # default windows torrent handler
            import win32api
            try:
                win32api.ShellExecute(0, "open", self.full_filename, "", config.TORRENT_DIR, 0)
                return True
            except:
               return False
            return True

