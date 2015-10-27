# Functions for getting and parsing webpages (TODO)
import urllib, urllib2
import re

# this is the function that will retrieve the source code of an url
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

# this is the function that retrieves the weath information
def GetWeatherInfo():
    page = GetPage("http://www.wunderground.com/q/zmw:48033.1.99999?MR=1")
    degreestart = page.find("Southfield, MI | ")
    degrees = page[degreestart+17:degreestart+21]
    status = page[degreestart+29:page.find("\"", degreestart+29)]
    return degrees, status
