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
from db import Config


class BaseCommand(object):
    def __init__(self, store):
        self.store = store
        self.parser = self.create_parser()
        self.options = {}

    def create_parser(self):
        raise NotImplementedError()

    def check_args(self, args):
        return False

    def show_help(self):
        print self.parser.format_help()

    def run(self):
        raise NotImplementedError()

    def get_config(self, varname):
        var = self.store.find(Config, Config.varname == unicode(varname)).one()
        if var:
            return var.value
        else:
            return ""

    def _best_value(self, opt, config_var, default):
        if opt:
            return opt

        tmp = self.get_config(config_var)
        if tmp:
            return tmp

        return default

