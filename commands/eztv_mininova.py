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
from base import BaseCommand
from optparse import OptionParser
from db import Show, Episode

EZTV_MININOVA_RSS="http://www.mininova.org/rss.xml?user=eztv"

class Command(BaseCommand):
    def __init__(self, store):
        super(Command, self).__init__(store)
        self.rx_episode = re.compile(u'(?P<episode_name>S[0-9]{2}E[0-9]{2})')
        self.rx_episode_alt = re.compile(u'(?P<episode_name>[0-9]{1,2}x[0-9]{1,2})')
        self.rx_episode_size = re.compile(u'Size:\s+([0-9.]+)')

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

    def run(self):
        print "save_torrents()"
        import feedparser

        try:
            if getattr(self.options, "file"):
                feed = feedparser.parse(self.options.file)
            elif getattr(self.options, "url"):
                feed = feedparser.parse(self.options.url)
            else:
                feed = feedparser.parse(EZTV_MININOVA_RSS)

            if not feed["entries"]:
                raise Exception()
        except Exception:
            print "Can't download rss or it's empty. Exiting"
            return

        shows = self.store.find(Show).order_by(Show.name)
        for entry in feed["entries"]:
            # adapta el row para que le valga a _save_new_episode
            row = {}
            row["name"] = entry["title"]

            # Importante: si no pongo list() el cursor queda abierto
            # y se queja de que hay 2 consultas SQL activas
            for show in list(shows):
                if show.match(row["name"]):
                    # En este feed el tamaño está como texto plano
                    # dentro del campo "summary"
                    try:
                        row["size"] = float(self.rx_episode_size.findall(entry["summary"])[0])
                    except IndexError:
                        print "File size not available. Skipping"
                        continue
                    except TypeError:
                        print "File size field corrupt. Skipping"
                        continue

                    row["url_torrent"] = [entry['enclosures'][0]["href"]]
                    # Prueba a descargar el fichero
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

