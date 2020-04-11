import requests
import sys
from bs4 import BeautifulSoup
import logger


class dlna_browser:
    def __init__(self, settings):
        self.config = settings
        self.server_address = 'http://%s:%s' % ( settings.server, settings.port)
    
def dlna_request( url, action, soap_mess ):
    headers={
        'User-Agent' : 'gupnp-av-cp GUPnP/0.18.1 DLNADOC/1.50',
        'Accept' : '',
        'Content-Type' : 'text/xml; charset="utf-8"',
        'SOAPAction' : '"urn:schemas-upnp-org:service:ContentDirectory:1#%s"' % action,
        'Accept-Language': 'en-us;q=1, en;q=0.5',
        'Accept-Encoding': 'gzip'
        }

    r = requests.post(url, headers=headers, data=soap_mess)
    body = BeautifulSoup(r.text, 'lxml')
    res = body.result.string
    res.replace("&lt;", "<")
    res.replace("&gt;", ">")
    nested = BeautifulSoup(res, 'lxml')
    return nested

class item:
    def __init__(self, container, item_xml, config):
        self.name = item_xml.find('dc:title').string
        self.oid = item_xml['id']
        self.container = container
        self.kind = item_xml.find('upnp:class').string
        self.config = config
        self.server_address = 'http://%s:%s' % ( config.server, config.port)

    def is_video(self):
        return self.kind == 'object.item.videoItem'

    def is_audio(self):
        return self.kind == 'object.item.audioItem.musicTrack'
        
    def indent_print(self, to, depth):
        offset = ''.join([' ' for i in range(depth * 2)])
        to.write(offset + self.name + "<" + str(self.oid) + ">\n")

    def lookup_url(self):
        soap_envelope='<?xml version="1.0" encoding="UTF-8" ?>'\
            '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">'\
        '<s:Body>'\
        '<u:Search xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">'\
        '<ContainerID>' + self.oid + '</ContainerID>'\
        '<SearchCriteria></SearchCriteria>'\
        '<Filter>*</Filter>'\
        '<StartingIndex>0</StartingIndex>'\
        '<RequestedCount>100</RequestedCount>'\
        '<SortCriteria></SortCriteria>'\
        '</u:Search>'\
        '</s:Body>'\
        '</s:Envelope>'

        info = dlna_request('%s/ctl/ContentDir' % self.server_address, 'Search', soap_envelope )
        return info.res.string

class folder:
    def __init__(self, name, config, oid='0', parent=None):
        self.name = name
        self.oid = oid
        self.children = []
        self.files = []
        self.parent = parent
        self.config = config
        self.server_address = 'http://%s:%s' % ( config.server, config.port)
    
    def subfolders(self):
        for c in self.children:
            yield c.name

    def file_names(self):
        for f in self.files:
            yield f.name
            
    def indent_print(self, to, depth = 0):
        offset = ''.join([' ' for i in range(depth * 2)])
        to.write(offset + self.name + "<" + str(self.oid) + ">\n")
        for c in self.children:
            c.indent_print( to, depth + 1 )
        for f in self.files:
            f.indent_print( to, depth )
            
    def fetch_contents(self, debug_to=None):
        response = self.query_server()
        if debug_to is not None:
            debug_to.write(response.prettify()+"\n")
        files = response.find_all('item')
        self.files = []
        for f in files:
            self.files += [ item(self,f, self.config) ]            
        subfolders = response.find_all('container')
        self.children = []
        for s in subfolders:
            self.children += [ folder(s.find('dc:title').string, self.config, s['id'], self) ]
            
    def query_server(self):
        soap_mess='<?xml version="1.0"?>'\
            '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">'\
            '<s:Body>'\
            '<u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1">'\
            '<ObjectID>' + str(self.oid) + '</ObjectID>'\
            '<BrowseFlag>BrowseDirectChildren</BrowseFlag>'\
            '<Filter>@childCount</Filter>'\
            '<StartingIndex>0</StartingIndex>'\
            '<RequestedCount>10000</RequestedCount>'\
            '<SortCriteria></SortCriteria>'\
            '</u:Browse>'\
            '</s:Body>'\
            '</s:Envelope>'
        return dlna_request('%s/ctl/ContentDir' % self.server_address, 'Browse', soap_mess )

