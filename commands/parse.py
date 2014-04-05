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
from db import Show

class Command(BaseCommand):
    """Parses a file name and return normalized data"""

    def create_parser(self):
        # -f filname [-s|-e]
        parser = OptionParser()

        parser.set_defaults(minsize=0, maxsize=0)

        parser.add_option('-f', '--filename', dest='filename',
                help='file name', metavar='FILENAME')
        parser.add_option('-s', '--show', action='store_true', default=False, dest='show',
                help='output the canonical show name', metavar='SHOW')
        parser.add_option('-e', '--episode', action='store_true', default=False, dest='episode',
                help='output the season/episode', metavar='EPISODE')

        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        self.filename = getattr(self.options, 'filename')
        print_show = getattr(self.options, 'show')
        print_episode = getattr(self.options, 'episode')

        # xor
        return self.filename and (print_show ^ print_episode)

    def run(self):
        pass

