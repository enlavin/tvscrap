#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TVScrap.py
"""

import re
import sys
from optparse import OptionParser
import storm.locals as st
from eztvefnet import Scrapper
from torrents import TorrentManager
from db import Show, Episode, connect_db

class TVScrap(object):
    """
    ideas:
    + tvscrap.py -r "Show" -x "rx" -m xx -n xx
    + tvscrap.py --set variable --value xxx
    + tvscrap.py --get variable
    + tvscrap.py --dump-config
    + tvscrap.py --list-shows
    + tvscrap.py --list-episodes SHOW
    + tvscrap.py -u http://www.eztv.it/index.php?main=show&id=575
    + tvscrap.py -f fulanico.html
    """
    def __init__(self):
        self.seriesdb = connect_db()
        self.store = st.Store(self.seriesdb)
        self.url = None
        self.file = None
        self.rx_episode = re.compile(u'(?P<episode_name>S[0-9]{2}E[0-9]{2})')
        self.rx_episode_alt = \
                re.compile(u'(?P<episode_name>[0-9]{1,2}x[0-9]{1,2})')


    def define_cmdline_options(self):
        """
        Opciones de linea de comandos para el parser
        """
        parser = OptionParser()
        parser.add_option("-l", "--list-shows", dest="listshows",
                action="store_true", help="show list of registered shows")
        parser.add_option("-e", "--list-episodes", dest="listepisodes",
                help="show list of downloaded episodes", metavar="SHOW")
        parser.add_option("-c", "--delete-show", dest="deleteshow",
                help="delete show", metavar="SHOW")
        parser.add_option("-d", "--delete-episode", dest="deleteepisode",
                help="delete episode", metavar="SHOW,EPISODE")
        parser.add_option("-r", "--register-show", dest="show",
                help="show name", metavar="SHOW")
        parser.add_option("-x", "--regexp", dest="regexp",
                help="regular expression", metavar="RX")
        #parser.add_option("-g", "--get", dest="getvar",
        #        help="", metavar="VARIABLE")
        #parser.add_option("-s", "--set", dest="setvar",
        #        help="", metavar="VARIABLE")
        #parser.add_option("-v", "--value", dest="value",
        #        help="", metavar="VALUE")
        #parser.add_option("-z", "--dump-config", dest="dump",
        #        action="store_true", help="", metavar="DUMP")
        parser.add_option("-u", "--force-url", dest="url",
                help="", metavar="URL")
        parser.add_option("-f", "--force-file", dest="file",
                help="", metavar="FILE")
        parser.add_option("-m", "--min-size", dest="minsize", type="float",
                help="min size in Mb", metavar="MINSIZE")
        parser.add_option("-n", "--max-size", dest="maxsize", type="float",
                help="max size in Mb", metavar="MAXSIZE")
        return parser

    def list_shows(self):
        """
        Muestra una lista de las series registradas
        """
        shows = self.store.find(Show).order_by(Show.name)
        for show in shows:
            print "'%s' '%s' (min: %3.1f Mb, max: %3.1f Mb)" % \
                    (show.name, show.regexp_filter,
                            show.min_size, show.max_size)

    def list_episodes(self, showname):
        """
        Muestra los episodios descargados/descargando de una serie
        """
        print "list_episodes(%s)" % showname
        for epi in self.store.find(Episode,
                Episode.show_id == Show.id,
                Show.name == unicode(showname)
                ).order_by(Show.name):
            print "%s|%s|%s|%3.1f" % \
                    (epi.name, epi.filename, epi.torrent, epi.size)

    def register_show(self, showname, regexp, minsize=0.0, maxsize=0.0):
        """
        Registra una nueva serie
        """
        if not minsize:
            minsize = 0.0
        if not maxsize:
            maxsize = 0.0

        show = self.store.find(Show, Show.name == unicode(showname)).one()
        if not show:
            show = Show()

        show.name = unicode(showname)
        show.regexp_filter = unicode(regexp)
        show.min_size = minsize
        show.max_size = maxsize
        self.store.add(show)
        self.store.commit()
        print "%s registrado con exito" % showname

    #def getvar(self, varname):
    #    print "getvar(%s)" % varname

    #def setvar(self, varname, value):
    #    print "setvar(%s,%s)" % (varname, value)

    #def dump_config(self):
    #    print "dump_config()"

    def download_new_episode(self, show, row):
        """
        Descarga un nuevo episodio
        """
        try:
            episode_name = self.rx_episode.findall(row["name"])[0]
        except IndexError:
            try:
                episode_name = self.rx_episode_alt.findall(row["name"])[0]
            except IndexError:
                print "No puedo averiguar el numero del capitulo"
                return

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
            print "Episodio %s:%s ya encolado o descargado" % \
                    (show.name, episode.name)
            return

        return episode


    def download_torrents(self):
        """
        Comprueba la lista de programas de una web con
        la lista de series que hay en BD y descarga
        los torrents de los capitulos que aun se tienen.
        """
        print "download_torrents()"

        try:
            scrapper = Scrapper()
            today = scrapper(url=self.url, file=self.file)
            if not today:
                raise Exception()
        except Exception:
            print "Can't download html. Exiting"
            return

        shows = self.store.find(Show).order_by(Show.name)
        for row in today:
            # Importante: si no pongo list() el cursor queda abierto
            # y se queja de que hay 2 consultas SQL activas
            for show in list(shows):
                if show.match(row["name"]):
                    # Prueba a descargar el fichero
                    if not show.check_size(row["size"]):
                        print u"%s: incorrecto (%3.1f Mb)" % \
                                (row["name"], row["size"])
                    else:
                        episode = self.download_new_episode(show, row)
                        if not episode:
                            break

                        torrentdl = TorrentManager(row["url_torrent"][0],
                                episode.torrent)
                        if torrentdl():
                            episode.queued = True
                            self.store.commit()

                        print "Download %s %s %s %s %s" % \
                                (show.name, episode.name,
                                 episode.torrent, row["url_torrent"][0],
                                 episode.filename)

    def delete_show(self, showname):
        """
        Borra una serie y sus capitulos
        """
        show = self.store.find(Show, Show.name == unicode(showname)).one()
        episodes = self.store.find(Episode, Episode.show_id == show.id)

        if not show or not episodes:
            print "No se encuentra el programa %s" % showname
        else:
            episodes.remove()
            self.store.remove(show)
            self.store.commit()

    def delete_episode(self, showname, episodename):
        """
        Borra un episodio de un capitulo de la BD
        """
        episode = self.store.find(Episode,
            Episode.name == unicode(episodename),
            Show.name == unicode(showname),
            Episode.show_id == Show.id).one()
        if episode:
            self.store.remove(episode)
            self.store.commit()
        else:
            print "No se encuentra el %s:%s" % (showname, episodename)


    def check_args(self, options):
        """
        Verifica que solo haya un comando activo y las
        dependencias de cada comando.
        """
        # Solo un comando activo
        commands = ['listshows', 'listepisodes', 'show',
                'deleteshow', 'deleteepisode', 'url', 'file']
        for cmd in commands:
            if not getattr(options, cmd):
                continue
            other_commands = [ccmd for ccmd in commands if ccmd != cmd]
            for rcmd in other_commands:
                if getattr(options, rcmd):
                    return False

        # Dependencias
        check_args = True
        if options.show and not options.regexp:
            check_args = False
        if (options.minsize or options.maxsize) and not options.show:
            check_args = False
        if options.file and options.url:
            check_args = False
        return check_args

    def run(self, new=True):
        """
        Ejecuta el scrapper
        """

        if new:
            if len(sys.argv) == 1:
                self.run_command('help')
                sys.exit(1)
            ret = self.run_command()
            return ret

        #######
        parser = self.define_cmdline_options()
        (options, _) = parser.parse_args()

        if not self.check_args(options):
            parser.print_help()
            exit(1)

        self.url = options.url
        self.file = options.file

        # TODO: refactorizar con clases comando
        if options.listshows:
            self.list_shows()
        elif options.listepisodes:
            self.list_episodes(options.listepisodes)
        elif options.show and options.regexp:
            self.register_show(options.show, options.regexp,
                    options.minsize, options.maxsize)
        #elif options.getvar:
        #    self.getvar(options.getvar)
        #elif options.setvar and options.value:
        #    self.setvar(options.setvar, options.value)
        #elif options.dump:
        #    self.dump_config()
        elif options.deleteshow:
            self.delete_show(options.deleteshow)
        elif options.deleteepisode:
            showname, episodename = [
                unicode(s.lstrip().rstrip())\
                        for s in options.deleteepisode.split(",")]
            self.delete_episode(showname, episodename)
        else:
            self.download_torrents()

    def get_command(self, name):
        """Busca el módulo que implementa un comando y devuelve la instancia inicializada o lanza un AttributeError en caso de error"""
        module = __import__('commands', {}, [], [name])
        klass = getattr(getattr(module, name), 'Command')

        return klass(self.store)

    def run_command(self, cmdname=None):
        try:
            if cmdname is None:
                cmdname = sys.argv[1]
            cmd = self.get_command(cmdname)
            if not cmd.check_args(sys.argv[1:]):
                cmd.show_help()
                sys.exit(1)

            ret = cmd.run()
        except AttributeError:
            self.run_command('help')
            sys.exit(1)

def main():
    """
    Lanza el programa
    """
    tvs = TVScrap()
    tvs.run(new=False)

if __name__ == '__main__':
    main()

