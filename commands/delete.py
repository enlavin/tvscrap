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
from base import BaseCommand
from optparse import OptionParser
from db import Show, Episode

class Command(BaseCommand):
    """Borra una serie y todos sus capitulos"""

    def create_parser(self):
        #
        parser = OptionParser()
        parser.add_option("-s", "--show", dest="show",
                help="show name", metavar="SHOW")
        parser.add_option("-e", "--episode", dest="episode",
                help="episode name SxxEyy or SxEE", metavar="EPISODE")
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return getattr(self.options, "show") or \
            (getattr(self.options, "show") and getattr(self.options, "episode"))

    def run(self):
        show = self.store.find(Show, Show.name == unicode(self.options.show)).one()
        if not show:
            print "No se encuentra el programa %s" % self.options.show
            return

        # borra un episodio
        if self.options.episode:
            episode = self.store.find(Episode,
                Episode.name == unicode(self.options.episode),
                Show.name == unicode(self.options.show),
                Episode.show_id == Show.id).one()
            self.store.remove(episode)
        else:
            # borra el show y sus episodios
            episodes = self.store.find(Episode, Episode.show_id == show.id)
            episodes.remove()
            self.store.remove(show)
        self.store.commit()

