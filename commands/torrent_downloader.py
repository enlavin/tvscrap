# -*- coding: utf-8 -*-
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

class TorrentServerConnectException(TorrentException):
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
                except TorrentServerConnectException:
                    print "Can't connect to server" 
                except TorrentAuthException:
                    print "Wrong credentials" 
                    return
                except TorrentURLException:
                    print "%s failed. Trying next url." % url


