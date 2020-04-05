Installing
==========
Blackjack is written using Python 3.

Blackjack has the following dependencies:
* BeautifulSoup 4
* LXML

sudo pip3 install beautifulsoup4 lxml

Config file syntax
==================

Blackjack uses a .INI file format.  The file begins with a [handlers] section
which defines various _handlers_ - a handler is a backend program which is
invoked to play media streamed from the DLNA server.  The following keys are
valid in the [handlers] section:

 * video
 * audio

For each handler, it is possible to configure it using a handler-specific keys
in a per-handler section.  For example, the only handler currently implemented
is the _mplayer_ handler.  This handler needs the path of the _mplayer_ binary
- by default, this is assumed to be /usr/bin/mplayer.  However, if your system
has installed mplayer at /usr/local/bin/mplayer, you can set up a
configuration as follows:

[mplayer]
path=/usr/local/bin/mplayer

Configurable settings for mplayer handler:
   * path - set the path of the mplayer binary
   * cache - set the size of the cache used for mplayer
