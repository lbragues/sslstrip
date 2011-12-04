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

http://sizeonedev.wordpress.com/

"""
from s1plugin.S1DummyPlugin import S1DummyPlugin
import httpagentparser

#Avoid TypeError on callbacks
#http://code.activestate.com/recipes/52304-static-methods-aka-class-methods-in-python/
class Callable:
	def __init__(self, anycallable):
		self.__call__ = anycallable

class S1Plugin(S1DummyPlugin):
	
	oslist={}
	browserlist={}
	
	def __init__(self):
		self.name = "OSFinder"
		self.author = "SizeOne"
		self.version = "1.0"
		self.s1version = ["1.0"] #only works for s1plugin ver 1.0
		self.url = "http://sizeone.net"
		self.help = "This plugin connects an ip address to an OS. And uses a callback to pass this info to other plugins"
		
	def initMyCallbacks(self):
		#register callbacks so other plugins can access
		#remember that the order that the plugins are loaded
		#may influence the result of callbacks
		self.registerCallBack("getOS",S1Plugin.getOS)
		self.registerCallBack("getBrowser",S1Plugin.getBrowser)
		
	def getOS(client):
		try:
			return S1Plugin.oslist[client]
		except KeyError:
			return ""
	#Avoid TypeError on callbacks
	getOS = Callable(getOS)

	def setOS(client,os):
		S1Plugin.oslist[client]=os
	setOS = Callable(setOS)

	def getBrowser(client):
		try:
			return S1Plugin.browserlist[client]
		except KeyError:
			return ""
	getBrowser = Callable(getBrowser)
		
	def setBrowser(client,browser):
		S1Plugin.browserlist[client]=browser
	setBrowser = Callable(setBrowser)

	def onClientConnection(self,host,headers,client,path,postData,url):
		ua="user-agent"
		os,browser = httpagentparser.simple_detect(headers[ua])
		S1Plugin.setOS(client,os)
		S1Plugin.setBrowser(client,browser)
		return host,headers,client,path,postData,url
