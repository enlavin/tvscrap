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
from db import Config

class Command(BaseCommand):
    """Show global config vars"""

    def create_parser(self):
        parser = OptionParser()
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return True
        
    def run(self):
        vars = self.store.find(Config).order_by(Config.varname)

        for var in vars:
            print "%s=%s" % (var.varname, var.value)

