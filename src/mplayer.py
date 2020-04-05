import subprocess
import os.path

class mplayer:
    def __init__(self):
        self.path = '/usr/bin/mplayer'
        self.cache = '10240'
        
    def reconfigure(self, conf):
        if 'path' in conf:
            path = conf['path']
            if not os.path.exists(path):
                print ("Path '%s' provided to mplayer handler does " \
                       "not exist" % path )
                sys.exit(1)
            self.path = path
        if 'cache' in conf:
            ival = int(conf['cache'])
            if ival < 0:
                print ("Invalid cache size %d provided" % ival)
                sys.exit(1)
            self.cache = str(ival)
            
    def play( self, URL ):
        argv = [ self.path, # Todo: other arguments
                 '-cache', self.cache,
                 URL
        ]
        with open('blackjack.mplayer.log', 'w') as log:
            ret = subprocess.call( argv, shell=False, stdout=log, stderr=subprocess.STDOUT )

def mplayer_init():
    return mplayer()
