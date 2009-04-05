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

class Command(BaseCommand):
    def create_parser(self):
        return OptionParser(usage="help")

    def check_args(self, args):
        (options, _) = self.parser.parse_args(args)
        return True

    def run(self):
        tvscrap_cmd = sys.argv[0]
        print """
%(tvscrap)s help
    Show this help
%(tvscrap)s register -s <show> -x <rx> [-m xx] [-n xx]
    Register a new show in DB
%(tvscrap)s shows
    List of registered shows
%(tvscrap)s episodes <show>
    Episode list for a show
%(tvscrap)s delete -s <show> [-e <episode>]
    Delete an episode/show from DB
%(tvscrap)s pending
    List of pending episodes
%(tvscrap)s eztv [-f file|-u url]
    Download torrents from eztv
%(tvscrap)s eztv_mininova [-f file|-u url]
    Download torrents from eztv RSS feed at mininova.org
%(tvscrap)s mldonkey [-m host] [-p port] [-u username] [-w password]
    Queue torrents in mldonkey
%(tvscrap)s transm [-m host] [-p port] [-u username] [-w password]
    Queue torrents in transmission
%(tvscrap)s windefault
    Queue torrents with Windows default torrent handler (only works in Windows)
%(tvscrap)s config
    Dump config variables
%(tvscrap)s set -n varname -v value
    Set/Update config variable
%(tvscrap)s unset -n varname
    Delete config variable
        """ % {"tvscrap": tvscrap_cmd}
