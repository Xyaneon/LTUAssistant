# Functions for getting and parsing webpages (TODO)
import urllib, urllib2
import re

def GetPage(url, cookies = None, headers = None, removeTags = False, getredirect=False):
    try:
        if cookies:
            req = urllib2.Request(url, urllib.urlencode(headers) if headers else None, {'Cookie':cookies})
        else:
            req = urllib2.Request(url, urllib.urlencode(headers) if headers else None)
        data = urllib2.urlopen(req, timeout=10)
        page = data.read()
        url = data.geturl()
        if removeTags:
            return re.sub("<.*?>", "", page)
        return url if getredirect else page
    except IOError:
        return None
