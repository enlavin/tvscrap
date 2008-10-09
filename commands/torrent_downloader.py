# -*- coding: utf-8 -*-
import sys
from telnetlib import Telnet
from base import BaseCommand
from optparse import OptionParser
from db import Episode, Show

class TorrentException(Exception):
    pass

class TorrentAuthException(TorrentException):
    pass

class TorrentURLException(TorrentException):
    pass

class TorrentCommand(BaseCommand):
    def run(self):
        episodes = self.store.find(Episode, Episode.queued == False, Episode.downloaded == False)

        if episodes.count() <= 0:
            print "No pending episodes in DB. Exiting."
            return

        for episode in episodes:
            print u"Sending %s to p2p" % (unicode(episode), )
            for url in episode.urls():
                try:
                    # Subclassify
                    self._send_command(url)
                    episode.queued = True
                    self.store.commit()
                    print "%s OK" % unicode(episode)
                    break
                except TorrentAuthException:
                    print "Wrong credentials" 
                    return
                except TorrentURLException:
                    print "%s failed. Trying next url." % url


