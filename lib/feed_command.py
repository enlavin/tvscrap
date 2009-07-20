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
import re
from lib.base import BaseCommand
from optparse import OptionParser
from db import Show, Episode
import tempfile
import os
import urllib

class FeedCommand(BaseCommand):
    def __init__(self, store):
        super(FeedCommand, self).__init__(store)
        self.rx_episode = re.compile(u'(?P<episode_name>S[0-9]{2}E[0-9]{2})')
        self.rx_episode_alt = re.compile(u'(?P<episode_name>[0-9]{1,2}x[0-9]{1,2})')

    def create_parser(self):
        # [-m url|-f file]
        parser = OptionParser()
        parser.add_option("-u", "--force-url", dest="url",
                help="", metavar="URL")
        parser.add_option("-f", "--force-file", dest="file",
                help="", metavar="FILE")

        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return (getattr(self.options, "url") and not getattr(self.options, "file")) or \
           (getattr(self.options, "file") and not getattr(self.options, "url")) or \
           (not getattr(self.options, "file") and not getattr(self.options, "url"))


    def _save_new_episode(self, show, row):
        """
        Encola en BD un nuevo episodio
        """
        try:
            # SxxEyy numbering scheme
            episode_name = self.rx_episode.findall(row["name"])[0]
        except IndexError:
            try:
                # SxEE numbering scheme
                episode_name = self.rx_episode_alt.findall(row["name"])[0]
                # Normalizes episode numbering to SxxEyy
                episode_name_parts = episode_name.split("x")
                episode_name = "S%02dE%02d" % tuple(int(n) for n in episode_name_parts[:2])
            except IndexError:
                print "Can't find episode number. Aborting."
                return

        episode_name = unicode(episode_name)
        episode = show.episodes.find(Episode.name == episode_name).one()
        if not episode:
            episode = Episode()
            episode.name = episode_name
            nospaces_name =  re.sub("\s+", ".", show.name.lstrip().rstrip())
            episode.filename = u"%s.%s.avi" % (nospaces_name, episode_name)
            episode.torrent = u"%s.%s.torrent" % (nospaces_name, episode_name)
            episode.size = row["size"]
            episode.show = show
            episode.queued = False
            episode.downloaded = False
            episode.url = "\n".join(row["url_torrent"])
            self.store.add(episode)
            self.store.flush()
            self.store.commit()
            return episode
        #elif episode.queued or episode.downloaded:
        else:
            print "Episodio %s:%s already queued or downloaded" % \
                    (show.name, episode.name)
        return

    def get_torrent_size(self, torrent_url):
        """download torrent from the url and try to extract size"""
        try:
            import hachoir_parser
            import hachoir_metadata
        except ImportError:
            return

        try:
            torrent = urllib.urlopen(torrent_url)
            ftmp = tempfile.mkstemp()
            try:
                os.write(ftmp[0], torrent.read())
                os.close(ftmp[0])
                
                metadata = hachoir_metadata.extractMetadata(
                    hachoir_parser.createParser(unicode(ftmp[1]), ftmp[1]))

                return metadata.get("file_size")
            finally:
                os.unlink(ftmp[1])
            
        except IOError:
            return


    def run(self):
        print "save_torrents()"

        self._config_feed()

        shows = self.store.find(Show).order_by(Show.name)
        for row in self._iter_feed():
            # Importante: si no pongo list() el cursor queda abierto
            # y se queja de que hay 2 consultas SQL activas
            for show in list(shows):
                if show.match(row["name"]):
                    # Prueba a descargar el fichero
                    if not row.has_key("size"):
                        # try to download .torrent file and analyze metadata to
                        # extract final file size
                        size = self.get_torrent_size(row["url_torrent"][0])
                        if not size:
                            print "Unable to get torrent size. Skipping"
                            continue
                        row["size"] = float(size) / 1048576.0

                    if not show.check_size(row["size"]):
                        print u"%s: incorrecto (%3.1f Mb)" % \
                                (row["name"], row["size"])
                    else:
                        episode = self._save_new_episode(show, row)
                        if not episode:
                            break

                        #torrentdl = TorrentManager(row["url_torrent"][0],
                        #        episode.torrent)
                        #if torrentdl():
                        #    episode.queued = True
                        #    self.store.commit()
                        #
                        print "Queued %s %s %s %s %s" % \
                                (show.name, episode.name,
                                 episode.torrent, episode.url,
                                 episode.filename)
