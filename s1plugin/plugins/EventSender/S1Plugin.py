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

http://sizeonedev.wordpress.com

"""
from s1plugin.S1DummyPlugin import S1DummyPlugin

class S1Plugin(S1DummyPlugin):
	def __init__(self):
		self.name = "Event Sender"
		self.author = "SizeOne"
		self.version = "1.0"
		self.s1version = ["1.0"] #only works for s1plugin ver 1.0
		self.url = "http://sizeone.net"
		self.help = "This plugin generates events that can be logged."
	
	def onResolveHost(self,client,host,result):
		#to do nothing return result as it is or remove function
		return result
	
	def onHostResolvedSuccess(self,client,address):
		#doesn't return anything
		pass
	
	def onHostResolvedError(self,client,error):
		#doesn't return anything
		pass
		
	def onCleanHeaders(self,client,headers,result):
		return result
		
	def onClientConnection(self,host,headers,client,path,postData,url):
		return host,headers,client,path,postData,url
	
	def onSendSpoofedFaviconResponse(self,client,icon_path):
		return icon_path
	
	def onProxy(self,client,host, method, path, postData, headers, port, ssl):
		return host, method, path, postData, headers, port
	
	def hijackConnection(self,client,url,clientConnection):
		return False
		
	def onVisitUrl(self,client,url,postData):
		pass