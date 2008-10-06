# tvscrap help
# tvscrap register -r <show> -x <rx> [-m xx] [-n xx]
# tvscrap shows
# tvscrap episodes <show>
# tvscrap delete <show> <episode>
# tvscrap eztv [-f file|-u url]

class BaseCommand(object):
    def __init__(self, store):
        self.store = store
        self.parser = self.create_parser()
        self.options = {}

    def create_parser(self):
        raise NotImplementedError #pass

    def check_args(self, args):
        return False

    def show_help(self):
        print self.parser.format_help()

    def run(self):
        raise NotImplementedError #pass


