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
    import feedparser
except ImportError:
    print "feedparser support not installed. Try easy_install feedparser."
    import sys
    sys.exit(1)

import re
from optparse import OptionParser
from db import Show, Episode
from lib.feed_command import FeedCommand

EZTV_BTCHAT_RSS="http://rss.bt-chat.com/?group=3&cat=9"

class Command(FeedCommand):
    def __init__(self, store):
        super(Command, self).__init__(store)
        self.rx_episode_size = re.compile(u'Size:\s+([0-9.]+)')

    def _config_feed(self):
        import feedparser

        if getattr(self.options, "file"):
            self.feed = feedparser.parse(self.options.file)
        elif getattr(self.options, "url"):
            self.feed = feedparser.parse(self.options.url)
        else:
            self.feed = feedparser.parse(EZTV_BTCHAT_RSS)

        if not self.feed["entries"]:
            raise Exception()

    def _iter_feed(self):
        for entry in self.feed["entries"]:
            yield {
                "name": entry["title"].replace(u".", u" "),
                "url_torrent": [entry['link']],
            }

