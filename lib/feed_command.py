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
from optparse import OptionParser
import os
import re
import requests
import tempfile

from db import Show, Episode
from lib.base import BaseCommand
from lib.episodes import get_episode_number, InvalidEpisodeName


class FeedCommand(BaseCommand):
    def __init__(self, store):
        super(FeedCommand, self).__init__(store)

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
        queues a new episode
        """
        try:
            episode_name = get_episode_number(row['name'])
        except InvalidEpisodeName:
            print("Can't find episode number. Aborting.")
            return

        episode = self.store.find_episode_by_number(show.name, episode_name)
        if not episode:
            nospaces_name = re.sub("\s+", ".", show.name.lstrip().rstrip())
            episode = Episode(
                id=-1,
                show_name=show.name,
                name=episode_name,
                show_id=show.id,
                url="\n".join(row["url_torrent"]),
                filename="{}.{}.avi".format(nospaces_name, episode_name),
                torrent="{}.{}.torrent".format(nospaces_name, episode_name),
                size=row["size"],
                queued=False,
                downloaded=False,
            )
            self.save_episode(episode)
            return episode
        #elif episode.queued or episode.downloaded:
        else:
            print("Episodio {0}:{1} already queued or downloaded".format(
                show.name, episode.name))
        return

    def get_torrent_size(self, torrent_url):
        """download torrent from the url and try to extract size"""
        try:
            import gzip
            import StringIO
            import hachoir_parser
            import hachoir_metadata
        except ImportError:
            return

        try:
            torrent = requests.get(torrent_url, timeout=60)
            ftmp = tempfile.mkstemp()
            try:
                if torrent.status_code != 200:
                    return

                torrent_data = torrent.text
                try:
                    sio = StringIO.StringIO(torrent_data)
                    gzfile = gzip.GzipFile(fileobj=sio)
                    torrent_data = gzfile.read()
                except IOError:
                    pass

                os.write(ftmp[0], torrent_data)
                os.close(ftmp[0])

                metadata = hachoir_metadata.extractMetadata(
                    hachoir_parser.createParser(unicode(ftmp[1]), ftmp[1]))

                if metadata:
                    return metadata.get("file_size")

                return None
            finally:
                os.unlink(ftmp[1])

        except IOError:
            return

    def run(self):
        print("save_torrents()")

        self._config_feed()

        shows = self.store.all_the_shows()
        for row in self._iter_feed():
            # Importante: si no pongo list() el cursor queda abierto
            # y se queja de que hay 2 consultas SQL activas
            for show in list(shows):
                if show.match(row["name"]):
                    # Prueba a descargar el fichero
                    if not 'size' in row or row.get("size", 0) <= 0:
                        # try to download .torrent file and analyze metadata to
                        # extract final file size
                        size = self.get_torrent_size(row["url_torrent"][0])
                        if not size:
                            print("Unable to get torrent size. Skipping")
                            continue
                        row["size"] = float(size) / 1048576.0

                    if not show.check_size(row["size"]):
                        print("{0}: incorrecto ({1:3.1f}Mb)".format(
                            row["name"], row["size"]))
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
                        print("Queued {} {} {} {} {}".format(
                            show.name, episode.name, episode.torrent,
                            episode.url, episode.filename))

