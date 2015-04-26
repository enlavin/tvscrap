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
import sys
from lib.base import BaseCommand
from optparse import OptionParser
from db.models import Show


class Command(BaseCommand):
    """Registra una nueva serie en la BD"""

    def create_parser(self):
        # -r "Show" -x "rx" [-m xx] [-n xx]
        parser = OptionParser()

        parser.set_defaults(minsize=0, maxsize=0)

        parser.add_option("-s", "--show", dest="show",
                help="show name", metavar="SHOW")
        parser.add_option("-x", "--regexp", dest="regexp",
                help="regular expression", metavar="RX")
        parser.add_option("-m", "--min-size", dest="minsize", type="float",
                help="min size in Mb", metavar="MINSIZE")
        parser.add_option("-n", "--max-size", dest="maxsize", type="float",
                help="max size in Mb", metavar="MAXSIZE")

        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        args_present = getattr(self.options, 'regexp') and getattr(self.options, 'show')
        minmax_ok = getattr(self.options, 'minsize') <= getattr(self.options, 'maxsize')
        return args_present and minmax_ok

    def run(self):
        show = self.store.find_show(self.options.show)
        if not show:
            show = Show()

        show.name = self.options.show
        show.regexp_filter = self.options.regexp
        show.min_size = self.options.minsize
        show.max_size = self.options.maxsize
        self.store.save_show(show)
        print("{} successfully registered".format(self.options.show))
