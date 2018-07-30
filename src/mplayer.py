import subprocess

class mplayer:
    def __init__(self):
        self.path = '/usr/bin/mplayer' # Todo: resolve properly

    def play( self, URL ):
        argv = [ self.path, # Todo: other arguments
                 '-cache', '1024', # 1MB - to be tuned
                 URL
        ]
        with open('blackjack.mplayer.log', 'w') as log:
            ret = subprocess.call( argv, shell=False, stdout=log, stderr=subprocess.STDOUT )

def mplayer_init():
    return mplayer()
