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
    """Set a global config var"""

    def create_parser(self):
        parser = OptionParser()
        parser.add_option('-n', '--name', dest='name',
                help='variable name', metavar='NAME')
        parser.add_option('-v', '--value', dest='value',
                help='variable value', metavar='VALUE')
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return getattr(self.options, 'name') and getattr(self.options, 'value')
        
    def run(self):
        var = self.store.find(Config, Config.varname == unicode(self.options.name)).one()
        if var:
            var.value = unicode(self.options.value)
            print "Updating %s=%s" % (var.varname, var.value)
        else:
            var = Config()
            var.varname = unicode(self.options.name)
            var.value = unicode(self.options.value)
            self.store.add(var)
            print "Setting %s=%s" % (var.varname, var.value)
        self.store.commit()

