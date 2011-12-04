#!/usr/bin/env python

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
import os
import types
import logging
import sqlite3
import hashlib

gVersion="1.0"

class S1PluginManager():
	
	def __init__(self):
		self.pluginList=[]
		self.callbackList={}
		#----- init sqlite settings database ----------------
		self.conn = sqlite3.connect('s1plugin/settings.db')
		#----- Load all modules -----------------------------
		if(os.path.exists("s1plugin/plugins")):
			#list directory
			lstd = os.listdir("s1plugin/plugins")
			dir = []
			for d in lstd:
				source=os.path.abspath("s1plugin/plugins")+os.sep + d
				if(os.path.isdir(source) and os.path.exists(source+os.sep+"__init__.py")):
					dir.append(d)
			#load modules
			for d in dir:
				logging.warning("------ Loading ["+d+"] --------------------------")
				name = "s1plugin.plugins."+d+".S1Plugin"
				mod = __import__(name)
				components = name.split('.')
				for comp in components[1:]:
					mod = getattr(mod, comp)
				plug=mod.S1Plugin()
				plug.setCallbackFunctions(self)
				plug.initMyCallbacks()
				logging.warning("Name: "+plug.getName()+" "+plug.getVersion())
				logging.warning("Author: "+plug.getAuthor())
				logging.warning("Url: "+plug.getUrl())
				logging.warning(plug.getHelp())
				if(plug.willWork(gVersion)):
					print "[S1PluginManager] "+plug.getName()+" "+plug.getVersion()+" loaded!"
					logging.warning("[Success] Plugin loaded!")
					self.pluginList.append(plug)
				else:
					print "[S1PluginManager] ERROR "+plug.getName()+" not loaded!"
					logging.error("[Error] plugin not loaded!")
					print "[S1PluginManager] This plugin will only work with s1plugin "+str(plug.getVersions())
					logging.error("This plugin will only work with s1plugin "+str(plug.getVersions()))
		print "S1Plugin "+gVersion+", mod by SizeOne"
	# ------- DATABASE --------------------------------------------
	def createDatabase(self,tableName):
		#check if table is created
		c = self.conn.cursor()
		try:
			c.execute('SELECT * FROM '+tableName+";")
		except sqlite3.OperationalError:
			#table doesnt exist create
			c.execute('CREATE TABLE '+tableName+' (id INTEGER PRIMARY KEY, key VARCHAR(200), value VARCHAR(500));')
			self.conn.commit()
		c.close()
	
	def storeValue(self,pluginName,pluginVersion,key,value):
		tname="t_"+(hashlib.sha1(pluginName+pluginVersion).hexdigest())
		self.createDatabase(tname)
		oldValue=self.readValue(pluginName,pluginVersion,key)
		c = self.conn.cursor()
		if(oldValue!=""):
			#update existing value
			c.execute('UPDATE '+tname+' SET value=(?) WHERE key=(?);',(value,key))
			self.conn.commit()
		else:
			#create new value
			c.execute('INSERT INTO '+tname+' (id, key, value) VALUES(NULL, (?), (?));',(key,value))
			self.conn.commit()
		c.close()
		
	def readValue(self,pluginName,pluginVersion,key):
		tname="t_"+(hashlib.sha1(pluginName+pluginVersion).hexdigest())
		self.createDatabase(tname)
		#try to get the value
		args = (key,)
		c = self.conn.cursor()
		try:
			c.execute('SELECT * FROM '+tname+' WHERE key=(?);',args)
			for row in c:
				return row[2]
		except sqlite3.OperationalError:
			#value doesn't exist
			return ""
		c.close()
	# --------------------------------------------------------------
	def registerCallBack(self,name,callback):
		self.callbackList[name]=callback
	
	def getAllCallbackNames(self):
		return self.callbackList.keys()	
	
	def callBack(self,name):
		return self.callbackList[name]
	
	def onResolveHost(self,client,host,result):
		for plugin in self.pluginList:
			result=plugin.onResolveHost(client,host,result)
		return result
		
	def onHostResolvedSuccess(self,client,address):
		for plugin in self.pluginList:
			plugin.onHostResolvedSuccess(client,address)

	def onHostResolvedError(self,client,error):
		for plugin in self.pluginList:
			plugin.onHostResolvedError(client,error)
	
	def onCleanHeaders(self,client,headers,result):
		for plugin in self.pluginList:
			result=plugin.onCleanHeaders(client,headers,result)
		return result
		
	def onClientConnection(self,host,headers,client,path,postData,url):
		for plugin in self.pluginList:
			host,headers,client,path,postData,url=plugin.onClientConnection(host,headers,client,path,postData,url)
			plugin.onVisitUrl(client,url,postData)
		return host,headers,client,path,postData,url
	
	def onSendSpoofedFaviconResponse(self,client,result):
		for plugin in self.pluginList:
			result=plugin.onSendSpoofedFaviconResponse(client,result)
		return result
	
	def onProxy(self,client,host, method, path, postData, headers, port, ssl):
		for plugin in self.pluginList:
			host, method, path, postData, headers, port=plugin.onProxy(client,host, method, path, postData, headers, port, ssl)
		return host, method, path, postData, headers, port
	
	def hijackConnection(self,client,url,clientConnection):
		for plugin in self.pluginList:
			if(plugin.hijackConnection(client,url,clientConnection)):
				return True
		return False
	
	def injectContent(self,client,contentType,data):
		for plugin in self.pluginList:
			data=plugin.injectContent(client,contentType,data)
		return data