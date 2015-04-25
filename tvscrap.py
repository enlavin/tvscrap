#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TVScrap.py

https://github.com/enlavin/tvscrap
"""
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
import socket
import sys
import storm.locals as st
from db import connect_db


class TVScrap(object):
    def __init__(self):
        self.seriesdb = connect_db()
        self.store = st.Store(self.seriesdb)

        # increase the default timeout to reduce the chance of timeouts
        # when the uploads are making outgoing connections slower
        socket.setdefaulttimeout(60)

    def get_command(self, name):
        """Find the module implementing a command and returns a initialized instance of Command"""
        module = __import__('commands', {}, [], [name])
        klass = getattr(getattr(module, name), 'Command')

        return klass(self.store)

    def run_command(self, cmdname=None):
        try:
            if cmdname is None:
                cmdname = sys.argv[1]
            cmd = self.get_command(cmdname)
        except AttributeError:
            self.run_command('help')
            sys.exit(1)

        if not cmd.check_args(sys.argv[1:]):
            cmd.show_help()
            sys.exit(1)

        ret = cmd.run()

    def run(self):
        if len(sys.argv) == 1:
            self.run_command('help')
            sys.exit(1)
        ret = self.run_command()
        return ret

def main():
    tvs = TVScrap()
    tvs.run()

if __name__ == '__main__':
    main()

