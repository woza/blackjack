#!/usr/bin/python3

from curses_ui import launch as curses_launch
from config import config
import argparse
import requests
import sys

parser = argparse.ArgumentParser(description='Blackjack DLNA Player')
parser.add_argument('--ui', choices=['curses'], default='curses')
parser.add_argument('--config', metavar='path', default='/usr/local/etc/blackjack.conf')

args = parser.parse_args()
conf = config(args.config)

try:
    if args.ui == 'curses':    
        curses_launch( conf )

except requests.exceptions.ConnectionError as e:
    print ("Failed to connect to DLNA server")
    sys.exit(1)



