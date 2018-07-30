#!/usr/bin/python

from curses_ui import launch as curses_launch
from mplayer import mplayer_init
import sys
import argparse

parser = argparse.ArgumentParser(description='Blackjack DLNA Player')
parser.add_argument('--server', metavar='IP')
parser.add_argument('--ui', choices=['curses'], default='curses')
# Add more UIs here in future
parser.add_argument('--video', choices=['mplayer'], default='mplayer')
# Add more video players here in future
# Add audio player here in future

args = parser.parse_args()

# Default values
handlers={
    'video' : mplayer_init()
}

if args.ui == 'curses':
    curses_launch( handlers )





