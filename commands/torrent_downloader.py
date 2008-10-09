# -*- coding: utf-8 -*-
import sys
from telnetlib import Telnet
from base import BaseCommand
from optparse import OptionParser
from db import Episode, Show

class MLException(Exception):
    pass

class MLAuthException(MLException):
    pass

class MLURLException(MLException):
    pass

class TorrentCommand(BaseCommand):
    def run(self):
        episodes = self.store.find(Episode, Episode.queued == False, Episode.downloaded == False)

        if episodes.count() <= 0:
            print "No pending episodes in DB. Exiting."
            return

        for episode in episodes:
            print u"Sending %s to mldonkey(%s:%s)" % (unicode(episode), self.host, self.port)
            for url in episode.urls():
                try:
                    # Subclassify
                    self._send_command(url)
                    episode.queued = True
                    self.store.commit()
                    print "%s OK" % unicode(episode)
                    break
                except MLAuthException:
                    print "Wrong credentials for %s:%s" % (self.host, self.port)
                    return
                except MLURLException:
                    print "%s failed. Trying next url." % url


