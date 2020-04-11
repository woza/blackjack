Introduction
============

Welcome to the Blackjack DLNA player!  This player exists because I could not
get reliable DLNA playback from my local server using any one of the host of
other players I tried (yes, including VLC).  Maybe it's my network, maybe my
server settings, but in the end I decided to follow the timeless advice of
Bender: "I'll build my own DLNA client - with blackjack!  And hookers!".  The
hookers are not yet implemented, but the client seems to work just fine.

Note that this is a _very lightweight_ client - it calls out to external media
players to perform the actual media playback.  Therefore, you'll need
something (currently, mplayer) installed on your system in addition to
Blackjack in order to actually play media.

Caveats
=======

This software is tested mostly through daily use on my home network, running
on OpenSUSE Linux.  I would be very surprised if it worked out of the box on
Windows, but it shouldn't be too hard to tweak.  It probably works on other
Linux distros, but I haven't tried.

Installing
==========
Blackjack is written using Python 3.  The following steps will get you from a
clean, minimal install of Ubuntu 19.04 Desktop (+OpenSSH server) to a running
instance of blackjack.

1. sudo apt install python3-pip mplayer
2. sudo pip3 install beautifulsoup4 lxml


Using
=====

Blackjack is driven from a config file.  By default, it looks for a
system-wide config file in /usr/local/etc/blackjack.conf - however, you can
override this by using the '--config' command-line argument.  For example:

./blackjack --config /some/other/path.conf

The configuration file is written using an INI syntax.  There is one mandatory
and several optional sections to the config file.

The mandatory section is the network information section, where two keys are
defined: 'server' provides the address of the DLNA server to query, and 'port'
defines which port to use when talking to the server.  An example network
section is:

    [network]
    server=192.168.30.207
    port=8201

The optional sections govern how media retrieved from DLNA are played to the
user.  Currently there are two media types defined: 'audio' and 'video'.  Each
type is associated with a _handler_ - the default (and currently only) handler
is the 'mplayer' handler.  So, the only valid handlers section currently looks
like this:

[handlers]
video=mplayer
audio=mplayer

It is not necessary to specify this section, though, as these are the default
settings for blackjack.

Each handler can have its own configuration directive.  The mplayer handler
has two configurable settings: the path to the mplayer binary, and the size of
the cache (specified in KB).  These are provided as so:

[mplayer]
path=/usr/bin/mplayer
cache=10240

(This example shows the default settings - you only need to include an
[mplayer] section if you want to move away from these defaults).

