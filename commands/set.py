import sys
from base import BaseCommand
from optparse import OptionParser
from db import Config

class Command(BaseCommand):
    """Set a global config var"""

    def create_parser(self):
        parser = OptionParser()
        parser.add_option('-n', '--name', dest='name',
                help='variable name', metavar='NAME')
        parser.add_option('-v', '--value', dest='value',
                help='variable value', metavar='VALUE')
        self.parser = parser
        return parser

    def check_args(self, args):
        (self.options, _) = self.parser.parse_args(args)
        return getattr(self.options, 'name') and getattr(self.options, 'value')
        
    def run(self):
        var = self.store.find(Config, Config.varname == unicode(self.options.name)).one()
        if var:
            var.value = unicode(self.options.value)
            print "Updating %s=%s" % (var.varname, var.value)
        else:
            var = Config()
            var.varname = unicode(self.options.name)
            var.value = unicode(self.options.value)
            self.store.add(var)
            print "Setting %s=%s" % (var.varname, var.value)
        self.store.commit()

