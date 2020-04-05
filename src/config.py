import os.path
import configparser
from mplayer import mplayer_init

class config:
    def __init__(self, path):
        self.handler_factory = {
            'mplayer' : mplayer_init()
        }
        self.handler_map = {
            'video' : 'mplayer',
            'audio' : 'mplayer'
        }
        self.server = None
        self.port = '8200'
        self.parse(path)

        self.handlers = {}
        for media_type,handler in self.handler_map.items():
            self.handlers[media_type] = self.handler_factory[handler]

        if self.server is None:
            print ("Server address not found - aborting")
            sys.exit(1)

    def parse( self, path ):
        conf = configparser.ConfigParser()
        conf.read(path)

        if 'network' in conf.sections():
            for key,value in conf['network'].items():
                if key == 'server':
                    self.server = value
                if key == 'port':
                    self.port = value

        if 'handlers' in conf.sections():
            for key,value in conf['handlers'].items():
                if value not in self.handler_factory:
                    print ("Unknown handler '%s' specified for media "\
                           "type '%s'" % (value,key))
                    sys.exit(1)
                self.handler_map[key] = value

        for media_type,handler in self.handler_map.items():
            if handler in conf.sections():
                self.handler_factory[handler].reconfigure(conf[handler])
