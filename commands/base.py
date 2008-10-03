# tvscrap help
# tvscrap register -r <show> -x <rx> [-m xx] [-n xx]
# tvscrap shows
# tvscrap episodes <show>
# tvscrap delete <show> <episode>
# tvscrap eztv [-f file|-u url]

class BaseCommand(object):
    def __init__(self, store):
        self.store = store

    def create_parser(self):
        raise NotImplementedError #pass

    def run(self, options):
        raise NotImplementedError #pass


