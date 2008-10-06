import sys
from base import BaseCommand
from optparse import OptionParser
from db import Config

class Command(BaseCommand):
    """Delete a global config var"""

    def create_parser(self):
        parser = OptionParser()
        parser.add_option('-n', '--name', dest='name',
                help='variable name', metavar='NAME')
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return getattr(self.options, 'name')
        
    def run(self):
        var = self.store.find(Config, Config.varname == unicode(self.options.name)).one()
        if var:
            print "Deleting config var: %s" % self.options.name
            self.store.remove(var)
            self.store.commit()
        else:
            print "Can't find config var: %s" % self.options.name

