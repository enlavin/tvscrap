# tvscrap help
# tvscrap register -r <show> -x <rx> [-m xx] [-n xx]
# tvscrap shows
# tvscrap episodes <show>
# tvscrap delete <show> <episode>
# tvscrap eztv [-f file|-u url]
class BaseCommand(object):
    def run(self, options):
        raise NotImplementedError #pass


