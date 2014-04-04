= TV Scrapper =

TVScrap.py is a tool to automate the download of weekly shows using eztv.it and bittorrent.


== Features ==

* [[http://mldonkey.sourceforge.net/Main_Page|MLDonkey]] support (using telnet)
* [[http://www.transmissionbt.com|Transmission]] support (via [[http://www.bitbucket.org/blueluna/transmissionrpc/|transmissionrpc]] module)
* Windows support (uses Windows Shell and the default handler of .torrent files)
* Modular: can be easily extended with new commands (RSS feeds, new P2P clients, ...).

== Prerequisites ==

TVScrap.py requires a recent [[http://python.org|Python]] distribution (tested with 2.4, 2.5 and 2.6) and the [[https://storm.canonical.com/|Storm ORM]]:

{{{
#!bash
$ easy_install -U storm
}}}

Also uses [[http://crummy.com/software/BeautifulSoup|BeautifulSoup]] HTML parser.

{{{
#!bash
$ easy_install -U BeautifulSoup
}}}

If you want [[http://www.transmissionbt.com|transmission]] support you have to install [[http://www.bitbucket.org/blueluna/transmissionrpc/wiki/Home|transmission json-rpc]] module:

{{{
#!bash
easy_install -U transmissionrpc
}}}

To fetch shows from RSS (mininova.org EZTV feed only at the moment) you will need feedparser:

{{{
#!bash
easy_install feedparser
}}}

To use [[http://twitter.com/eztv_it|EZTV Twitter]] timeline to get new torrents you will need python-twitter and hachoir:

{{{
#!bash
easy_install python-twitter hachoir_parser hachoir_metadata
}}}

In Windows you will also need "[[http://sourceforge.net/project/showfiles.php?group_id=78018&package_id=79063&release_id=616849|Python for Windows Extensions]]".

== Installation ==

Create a default empty database (SQLite).

In Linux or POSIX:

{{{
#!bash
$ mkdir  $HOME/.tvscrap
$ cp migration/tvscrap_template.db $HOME/.tvscrap/tvscrap.db
}}}

In Windows (using command-line)
{{{
#!bat
c:\tvscrap> mkdir "%HOMEDRIVE%\%HOMEPATH%\.tvscrap"
c:\tvscrap> copy migration\tvscrap_template.db "%HOMEDRIVE%\%HOMEPATH%\.tvscrap"
}}}
== Command line help ==

Try to run the help command:

{{{
#!bash
$ python tvscrap.py help

tvscrap help
    Show this help
tvscrap register -s <show> -x <rx> [-m xx] [-n xx]
    Register a new show in DB
tvscrap shows
    List of registered shows
tvscrap episodes <show>
    Episode list for a show
tvscrap delete -s <show> [-e <episode>]
    Delete an episode/show from DB
tvscrap pending
    List of pending episodes
tvscrap eztv [-f file|-u url]
    Download torrents from eztv
tvscrap eztv_mininova [-f file|-u url]
    Download torrents from mininova.org EZTV RSS feed
tvscrap eztv_btchat [-f file|-u url]
    Download torrents from bt-chat.com EZTV RSS feed
tvscrap mldonkey [-m host] [-p port] [-u username] [-w password]
    Queue torrents in mldonkey
tvscrap transm [-m host] [-p port] [-u username] [-w password]
    Queue torrents in transmission
tvscrap windefault
    Queue torrents using the default .torrent handler in Windows
tvscrap config
    Dump config variables
tvscrap set -n varname -v value
    Set/Update config variable
tvscrap unset -n varname
    Delete config variable
}}}

== Examples ==

Register a new show and download it only if the size of the file is between 150 and 300 MB

{{{
#!bash
$ python tvscrap.py register -s "The.Big.Bang.Theory" -x "^The\s+Big\s+Bang\s+Theory\s+" -m 150 -n 300
}}}

List registered shows:

{{{
#!bash
$ python tvscrap.py shows

'Dexter' '^Dexter\s+' (min: 350.0 Mb, max: 650.0 Mb)
'The Big Bang Theory' '^The\s+Big\s+Bang\s+Theory\s+' (min: 150.0 Mb, max: 400.0 Mb)
...
}}}

Configure default user/password of your mldonkey account (this has to be done only once):

{{{
#!bash
$ python tvscrap.py set mldonkey.username "admin"
$ python tvscrap.py set mldonkey.password "pass"
$ python tvscrap.py set mldonkey.host "localhost"
$ python tvscrap.py set mldonkey.port "4000"
}}}

Fetch torrents from http://eztv.it and feed them to [[http://mldonkey.sourceforge.net/Main_Page|MLDonkey]]:

{{{
#!bash
$ python tvscrap.py eztv
$ python tvscrap.py mldonkey
}}}

There is a analogous set of variables for [[http://www.transmissionbt.com|transmission]] support (transmission.host, transmission.port, etc). The command to queue the torrents in transmission is:

{{{
#!bash
$ python tvscrap.py transm
}}}

You will need to enable the web interface of Transmission, by default in port 9091.

Configure cron to check for new shows every 6 hours:

{{{
#!bash
$ crontab -e

# And then add
12 */6 * * * python /path/to/tvscrap.py eztv_twitter; python /path/to/tvscrap.py transm
}}}

Or if you are using Windows and have a bittorrent client already configured you can use a Windows Scheduled Task that launchs:
{{{
#!bash
tvscrap.py eztv_twitter
tvscrap.py windefault
}}}

== Disclaimer ==

{{http://enlavin.com/media/cuadritos/img/works-on-my-machine-starburst.png|Works on my machine}}

