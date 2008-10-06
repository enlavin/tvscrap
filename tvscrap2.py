#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TVScrap2.py
"""

import re
import sys
import storm.locals as st
from db import Show, Episode, connect_db

class TVScrap(object):
    def __init__(self):
        self.seriesdb = connect_db()
        self.store = st.Store(self.seriesdb)

    def run(self):
        """
        Ejecuta el scrapper
        """
        if len(sys.argv) == 1:
            self.run_command('help')
            sys.exit(1)
        ret = self.run_command()
        return ret

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
    tvs.run()

if __name__ == '__main__':
    main()

