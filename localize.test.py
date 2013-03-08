#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Test msgu.localize.Localize
  Real world usage scenarios:
	1 change console text locale
	2 change GUI text locale: basic
	3 change GUI text locale: ui loaded from gtkBuilder
"""
from __future__ import print_function
import pygtk
pygtk.require('2.0')
import gtk, gobject

from localize import Localize

class HelloWorld(object):
	def hello(self, widget, data=None):
		print( _("About") )
	
	def delete_event(self, widget, event, data=None):
		print("delete event occurred")
		return False
	
	def destroy(self, widget, data=None):
		print("quiting app")
		self.window.hide()
		self.mainloop.quit()
	
	def ja(self, widget, data=None):
		self.loc.language = "ja"
		self.restart = True
		self.destroy(self.window)
	
	def en(self, widget, data=None):
		self.loc.language = "en"
		self.restart = True
		self.destroy(self.window)
	
	def make_hbox(self, homogeneous, spacing, expand, fill, padding):
		box = gtk.HBox(homogeneous, spacing)
		button = gtk.Button( "ja" )
		button.connect("clicked", self.ja, None)
		box.pack_start(button, expand, fill, padding)
		del button
		
		button = gtk.Button( "en" )
		button.connect("clicked", self.en, None)
		box.pack_start(button, expand, fill, padding)
		del button
		return box
	
	def reload(self):
		self.button
		self.window.queue_draw()
		while gtk.events_pending():
			gtk.main_iteration_do(True)
		self.window.hide()
		self.window.show_all()
	
	def __init__(self, localize):
		"""Constructor"""
		
		#Stored, for when the time comes around to quit the mainloop.
		self.mainloop = None
		
		self.restart = False
		self.loc = localize
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.set_border_width(10)
		self.window.connect("destroy", self.destroy)
		vbox1 = gtk.VBox(False, 0)
		
		#Make horizontal box
		homogeneous = False
		spacing = 0
		expand = False
		fill = False
		padding = 0
		hbox1 = self.make_hbox(homogeneous, spacing, expand, fill, padding)
		vbox1.pack_start(hbox1, False, False, 0)
		
		self.button = gtk.Button( _("About") )
		self.button.connect("clicked", self.hello, None)
		self.button.connect_object("clicked", gtk.Widget.destroy, self.window)
		vbox1.pack_start(self.button, False, False, 0)
		
		self.window.add(vbox1)
		self.window.show_all()
	
	def __del__(self):
		self.window.hide()

if __name__ == '__main__':
	localize = Localize(app_name="msgu")
	localize.language = "ja"
	
	#Scenario #1
	bolGettextTest = False
	if bolGettextTest:
		#Changes the current / installed language
		localize.language = "ja"
		
		#"About" is in the msgu.mo catalogs. In both English & Japanese
		print(_("About"))
		localize.language = "en"
		print(_("About"))
	
	#Test whether localized in specific language 
	bolContainsTest = False
	if bolContainsTest is True:
		if "ja" in localize:
			print("Supports Japanese")
	
	#Loops thru
	bolIterTest = False
	if bolIterTest is True:
		for loc in localize:
			print(loc)
	
	#Scenario #2
	# This while loop demonstrates how to restart a gtk app
	# The restarted app will display in the selected locale.
	restart = True
	while restart is not False:
		print ("intializing hello")
		hello = HelloWorld(localize)
		print ("calling hello.main")
		""" WARNING to gtk developers
			Why not use gtk.main() here?
			
			On ubuntu, the osd-notify (Desktop notification Specification)
			https://wiki.ubuntu.com/NotifyOSD
			has a hardcoded limit of 20 notifications. After that the notifications are 
			not displayed nor put into the notification queue.
			Most Python developers use pynotify for desktop notifications. pynotify is 
			too naive to handle a notification upper limit.
			So the lower level interface **dbus** is used.
			
			dbus uses:
			
			from dbus.mainloop.glib import DBusGMainLoop
			
			glib is gobject, not gtk.
			So discourage the use of both pynotify and gtk.main() to start main loop."""
		hello.mainloop = gobject.MainLoop()
		hello.mainloop.run()
		"""Read the flag whether or not to restart the main loop.
		Once restarted the locale strings will appear in the choosen locale."""
		print ( "hello.restart", hello.restart )
		restart = hello.restart
		del hello
