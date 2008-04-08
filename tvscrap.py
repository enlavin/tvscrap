#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from optparse import OptionParser
from storm.locals import *
from eztvefnet import Scrapper
from torrents import TorrentManager
from db import Show, Episode, Config, connect_db
from config import *

# ideas:
# + tvscrap.py --register-show="Show" --regexp="rx" [--min-size=xx] [--max-size=xx]
# + tvscrap.py --set variable --value xxx
# + tvscrap.py --get variable
# + tvscrap.py --dump-config
# + tvscrap.py --list-shows
# + tvscrap.py --list-episodes SHOW

class TVScrap(object):
    def __init__(self):
        self.db = connect_db()
        self.store = Store(self.db)

    def define_cmdline_options(self):
        parser = OptionParser()
        parser.add_option("-l","--list-shows", dest="listshows", action="store_true", help="show list of registered shows")
        parser.add_option("-e","--list-episodes", dest="listepisodes", help="show list of downloaded episodes", metavar="SHOW")
        parser.add_option("-f","--delete-show", dest="deleteshow", help="delete show", metavar="SHOW")
        parser.add_option("-d","--delete-episode", dest="deleteepisode", help="delete episode", metavar="SHOW,EPISODE")
        parser.add_option("-r","--register-show", dest="show", help="show name", metavar="SHOW")
        parser.add_option("-x","--regexp", dest="regexp", help="regular expression", metavar="RX")
        parser.add_option("-g","--get", dest="getvar", help="", metavar="VARIABLE")
        parser.add_option("-s","--set", dest="setvar", help="", metavar="VARIABLE")
        parser.add_option("-v","--value", dest="value", help="", metavar="VALUE")
        parser.add_option("-u","--dump-config", dest="dump", action="store_true", help="", metavar="DUMP")
        parser.add_option("-m","--min-size", dest="minsize", type="float", help="min size in Mb", metavar="MINSIZE")
        parser.add_option("-n","--max-size", dest="maxsize", type="float", help="max size in Mb", metavar="MAXSIZE")
        return parser

    def list_shows(self):
        shows = self.store.find(Show).order_by(Show.name)
        for s in shows:
            print "'%s' '%s' (min: %3.1f Mb, max: %3.1f Mb)" % (s.name, s.regexp_filter, s.min_size, s.max_size)

    def list_episodes(self, showname):
        print "list_episodes(%s)" % showname
        for epi in self.store.find(Episode, Episode.show_id == Show.id, Show.name == unicode(showname)).order_by(Show.name):
            print "%s|%s|%s|%3.1f" % (epi.name, epi.filename, epi.torrent, epi.size)

    def register_show(self, showname, regexp, minsize=0.0, maxsize=0.0):
        if not minsize:
            minsize = 0.0
        if not maxsize:
            maxsize = 0.0

        try:
            show = self.store.find(Show, Show.name == unicode(showname)).one()
            if not show:
                show = Show()
        except:
            show = Show()

        try:
            show.name = unicode(showname)
            show.regexp_filter = unicode(regexp)
            show.min_size = minsize
            show.max_size = maxsize
            self.store.add(show)
            self.store.commit()
            print "%s registrado con exito" % showname
        except:
            print "Error al registrar un programa nuevo"

    def getvar(self, varname):
        print "getvar(%s)" % varname

    def setvar(self, varname, value):
        print "setvar(%s,%s)" % (varname, value)

    def dump_config(self):
        print "dump_config()"

    def download_torrents(self):
        print "download_torrents()"

        sc = Scrapper()
        for i in range(3):
            today = sc()
            if today:
                break

        shows = self.store.find(Show).order_by(Show.name)
        rx_episode = re.compile(u'(?P<episode_name>S[0-9]{2}E[0-9]{2})')
        rx_episode_alt = re.compile(u'(?P<episode_name>[0-9]{1,2}x[0-9]{1,2})')
        for row in today:
            # Importante: si no pongo list() el cursor queda abierto y se queja de que hay 2 consultas SQL activas
            for show in list(shows):
                if show.match(row["name"]):
                    # Prueba a descargar el fichero
                    if not show.check_size(row["size"]):
                        print u"%s: incorrecto (%3.1f Mb)" % (row["name"], row["size"])
                    else:
                        #import rpdb2; rpdb2.start_embedded_debugger('a', fAllowRemote=True, fAllowUnencrypted=True)
                        try:
                            episode_name = rx_episode.findall(row["name"])[0]
                        except:
                            episode_name = rx_episode_alt.findall(row["name"])[0]

                        episode = show.episodes.find(Episode.name == episode_name).one()
                        if not episode:
                            episode = Episode()
                            episode.name = episode_name
                            nospaces_name =  re.sub("\s+", ".", show.name.lstrip().rstrip())
                            episode.filename = "%s.%s.avi" % (nospaces_name, episode_name)
                            episode.torrent = "%s.%s.torrent" % (nospaces_name, episode_name)
                            episode.size = row["size"]
                            episode.show = show
                            episode.queued = False
                            episode.downloaded = False
                            self.store.add(episode)
                            self.store.flush()
                            self.store.commit()

                        if episode.queued or episode.downloaded:
                            print "Episodio %s:%s ya encolado o descargado" % (show.name, episode.name)
                            break

                        td = TorrentManager(row["url_torrent"][2], episode.torrent)
                        if td():
                            episode.queued = True
                            self.store.commit()

                        print "Download %s %s %s %s %s" % (show.name, episode_name, episode.torrent, row["url_torrent"][0], episode.filename)

    def delete_show(self, showname):
        try:
            import pdb; pdb.set_trace()
            show = self.store.find(Show, Show.name == unicode(showname)).one()
            episodes = self.store.find(Episode, Episode.show_id == show.id)

            episodes.remove()
            self.store.remove(show)
            self.store.commit()
        except:
            print "No se encuentra el programa %s" % showname

    def delete_episode(self, showname, episodename):
        try:
            episode = self.store.find(Episode,
                Episode.name == unicode(episodename),
                Show.name == unicode(showname),
                Episode.show_id == Show.id).one()
            if episode:
                self.store.remove(episode)
                self.store.commit()
        except:
            print "No se encuentra el %s:%s" % (showname, episodename)



    def check_args(self, options, args):
        # Solo un comando activo
        commands = ['listshows','listepisodes','show','getvar','setvar','dump','deleteshow','deleteepisode']
        for c in commands:
            if not getattr(options, c):
                continue
            other_commands = [cc for cc in commands if cc <> c]
            for rc in other_commands:
                if getattr(options, rc):
                    return False

        # Dependencias
        check_args = True
        if options.show and not options.regexp:
            check_args = False
        if (options.minsize or options.maxsize) and not options.show:
            check_args = False
        return check_args

    def run(self):
        parser = self.define_cmdline_options()
        (options, args) = parser.parse_args()

        if not self.check_args(options, args):
            parser.print_help()
            exit(1)

        if options.listshows:
            self.list_shows()
        elif options.listepisodes:
            self.list_episodes(options.listepisodes)
        elif options.show and options.regexp:
            self.register_show(options.show, options.regexp, options.minsize, options.maxsize)
        elif options.getvar:
            self.getvar(options.getvar)
        elif options.setvar and options.value:
            self.setvar(options.setvar, options.value)
        elif options.dump:
            self.dump_config()
        elif options.deleteshow:
            self.delete_show(options.deleteshow)
        elif options.deleteepisode:
            showname,episodename = [unicode(s.lstrip().rstrip()) for s in options.deleteepisode.split(",")]
            self.delete_episode(showname, episodename)
        else:
            self.download_torrents()

def main():
    tv = TVScrap()
    tv.run()

if __name__ == '__main__':
    main()

