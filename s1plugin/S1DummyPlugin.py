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
class S1DummyPlugin():
	def __init__(self):
		self.name = "Dummy Plugin" 
		self.author = "SizeOne"
		self.version = "1.0"
		self.s1version = ["1.0"] #only works for s1plugin ver 1.0
		self.url = "http://sizeone.net"
		self.help = "This plugin is here to the the default methods, doesn't do anything."
	
	#--- storage functions ----------------------------
	#some storage if needed
	def storeValue(self,key,value):
		self._storeValue(self.name,self.version,key,value)
		
	def readValue(self,key):
		return self._readValue(self.name,self.version,key)
	#--------------------------------------------------
	#--- empty functions ------------------------------
	def initMyCallbacks(self):
		pass
	#in case no manager is registered
	def registerCallBack(self,name,callback):
		pass
		
	def callBack(self,name):
		pass
	
	def getAllCallbackNames(self):
		return []
	#----------------------------------------
	
	# -------- Replace originals -------------------
	def setCallbackFunctions(self,mgr):
		self.registerCallBack=mgr.registerCallBack
		self.callBack=mgr.callBack
		self.getAllCallbackNames=mgr.getAllCallbackNames
		self._storeValue=mgr.storeValue
		self._readValue=mgr.readValue
	# ----------------------------------------------
	
	# -------- Getters and setters -----------------
	def getName(self):
		return self.name
	
	def getAuthor(self):
		return self.author
		
	def getVersion(self):
		return self.version
	
	def getVersions(self):
		return self.s1version
	
	def willWork(self,s1v):
		if(s1v in self.s1version):
			return True
		else:
			return False;
	
	def getUrl(self):
		return self.url
		
	def getHelp(self):
		return self.help
		
	# ----------------------------------------------
	
	# -------- Virtual Methods ---------------------
	def onResolveHost(self,client,host,result):
		#to do nothing return result as it is
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
		
	def injectContent(self,client,contentType,data):
		return data