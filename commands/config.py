# -*- coding: utf-8 -*-
import sys
from base import BaseCommand
from optparse import OptionParser
from db import Config

class Command(BaseCommand):
    """Show global config vars"""

    def create_parser(self):
        parser = OptionParser()
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return True
        
    def run(self):
        vars = self.store.find(Config).order_by(Config.varname)

        for var in vars:
            print "%s=%s" % (var.varname, var.value)

