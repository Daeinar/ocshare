#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Author: Philipp Jovanovic
Description: Command line tool to generate shared links for ownCloud files,
with clipboard support for OS X and Linux.
Date: 01 Feb 2014
Dependencies: Python 2.7.5+, ownCloud 6.0.1+, pbcopy (optionally, OS X), xclip
(optionally, Linux)
"""

import getpass
import os
import re
import sys
import subprocess
import urllib
import urllib2

# custom config
url = 'https://server-url/owncloud'
root = '/absolute/path/to/local/ownCloud/folder'
username = ''
password = ''

# fixed config
api_url = url + '/ocs/v1.php/apps/files_sharing/api/v1/shares'

def to_clipboard( data, prg ):
    try:
        p = subprocess.Popen( [ prg ], stdin=subprocess.PIPE )
        p.stdin.write(data)
        p.stdin.close()
        retcode = p.wait()
        print "Copied shared link to clipboard."
    except:
        print data

if __name__ == '__main__':

    assert len( sys.argv ) == 2

    if username == '' and password == '':
        username = raw_input('Username: ')
        password = getpass.getpass('Password: ')

    # parse file path
    print os.path.abspath( root )
    path = re.sub( root ,'/clientsync', os.path.abspath( sys.argv[1] ) )

    # send request
    p = urllib2.HTTPPasswordMgrWithDefaultRealm()
    p.add_password( None, api_url, username, password )
    handler = urllib2.HTTPBasicAuthHandler( p )
    opener = urllib2.build_opener( handler )
    urllib2.install_opener( opener )
    data = urllib.urlencode( { 'path' : path, 'shareType' : '3' } )
    page = urllib2.urlopen( api_url, data ).read()

    # extract link
    matchObj = re.search( '\<url\>.*\<\/url\>', page )
    link = re.sub( '(\<url\>|<\/url\>|amp\;)', '', matchObj.group() )

    # try to copy link to clipboard
    if sys.platform == 'darwin':
        to_clipboard( link, 'pbcopy' )
    elif sys.platform == 'linux':
        to_clipboard( link, 'xclip' )
    else:
        print link

