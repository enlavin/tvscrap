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
try:
    import twitter
except ImportError:
    print "twitter support not installed. Try easy_install python-twittwer."
    import sys
    sys.exit(1)

import re
from optparse import OptionParser
from db import Show, Episode

class Command(FeedCommand):
    def __init__(self, store):
        super(Command, self).__init__(store)

    def _config_feed(self):
        self.twapi = twitter.Api()
        
    def _iter_feed(self):
        # reverse-ordered-by-date tweet list
        for entry in self.twapi.GetUserTimeline("eztv_it"):
            try:
                size = float(self.rx_episode_size.findall(entry["summary"])[0])
            except IndexError:
                print "File size not available. Skipping"
                continue
            except TypeError:
                print "File size field corrupt. Skipping"
                continue

            yield {
                "name": entry["title"],
                "size": size,
                "url_torrent": [entry['enclosures'][0]["href"]],
            }

