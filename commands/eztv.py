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
from lib.eztvefnet import Scrapper
from lib.feed_command import FeedCommand


class Command(FeedCommand):
    def _config_feed(self):
        scrapper = Scrapper()
        self.today = scrapper(url=self.options.url, file=self.options.file)
        if not self.today:
            raise Exception()

    def _iter_feed(self):
        for row in self.today:
            yield row

