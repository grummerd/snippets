#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Switch between gettext locales on the fly
  docs.python.org/2/library/userdit.html#module-UserDict.DictMixin
	docs.python.org/2/library/collections.html#collections.MutableMapping
"""

from __future__ import print_function
import sys, gettext, gtk, gobject
import locale, glob, os.path
import collections
from config_xml import ConfigXML

try:
	from collections import MutableMapping
except ImportError:
	from UserDict import DictMixin as MutableMapping

class Localize(dict, MutableMapping):
	""" Switch between gettext locales on the fly"""
	def __init__(self, locale_path="", app_name="msgu"):
		self.app_name = app_name
		if len(locale_path)!=0:
			self.locale_path = locale_path
		else:
			self.locale_path = os.path.join(sys.prefix, 'local', 'share', 'locale')
		self._languages = {}
		self._language = None
		
		# http://stackoverflow.com/questions/10094335/how-to-bind-a-text-domain-to-a-local-folder-for-gettext-under-gtk3
		# https://github.com/dieterv/elib.intl/blob/master/lib/elib/intl/__init__.py
		locale.setlocale(locale.LC_ALL, '')
		locale.bindtextdomain(self.app_name, self.locale_path)
		locale.bind_textdomain_codeset(self.app_name, 'UTF-8')
		locale.textdomain(self.app_name)
		
		gettext.bindtextdomain(self.app_name, self.locale_path)
		gettext.bind_textdomain_codeset(self.app_name, 'UTF-8')
		gettext.textdomain(self.app_name)
		#_ = gettext.gettext
		print( "Using locale folder: {}".format(self.locale_path) )
		
		self.install()
		#self.update(locale_path, app_name)
		pass
	
	def __getitem__(self, strLocale):
		if type(key) not in [str, unicode]:
			raise TypeError("locale must be a string")
		if len ( self._languages.get(strLocale, "") )==0:
			#No translation by that name
			raise KeyError("No locale named %(locale)s" % {'locale': strLocale} )
		
		return self._languages.get(strLocale, "")
	
	def __contains__(self, strLocale):
		try:
			o = self._languages[strLocale]
		except KeyError:
			return False
		return o is not None
	
	def __repr(self):
		return "<%(class)s at %(id)s>" % {'id': id(self), 'class': self.__class__.__name__}
	
	def __iter__(self):
		return iter(self._languages)
	
	try:
		items = MutableMapping.iteritems
	except AttributeError:
		#Python 3
		items = MutableMapping.items
	
	def keys(self):
		return self._languages.keys()
	
	def __setitem__(self, strLocale, translation):
		if type(strLocale) not in [str, unicode]:
			raise TypeError("locale must be a string")
		if len ( self._languages.get(strLocale, "") )==0:
			#No translation by that name
			raise KeyError("No locale named %(locale)s" % {'locale': strLocale} )
		self._languages[strLocale] = translation
	
	def __delitem__(self, strLocale):
		if type(strLocale) not in [str, unicode]:
			raise TypeError("locale must be a string")
		if len ( self._languages.get(strLocale, "") )==0:
			#No translation by that name
			raise KeyError("No locale named %(locale)s" % {'locale': strLocale} )
		del self._languages[strLocale]
	
	def __len__(self):
		return len(self._languages)
	
	@property
	def language(self):
		""" Current language"""
		return self._language
	
	@language.setter
	def language(self, loc):
		""" Change current language"""
		try:
			self._languages[loc].install()
			self._language = loc
		except KeyError as why:
			pass
	
	def install(self):
		gettext.install(self.app_name, self.locale_path, unicode=True)
		languagePath = glob.glob( os.path.join(self.locale_path, '*') )
		locales = [ os.path.basename(loc) for loc in languagePath ]
		for strLocale in locales:
			try:
				t = gettext.translation(self.app_name, self.locale_path, languages=[strLocale] )
			except IOError:
				pass 
			else:
				self._languages[strLocale] = t
				#print(self.__class__.__name__ + ".install translation", strLocale, self._languages[strLocale])
				pass
		del languagePath, locales

import pygtk
pygtk.require('2.0')
import gtk
class HelloWorld(object):
	def hello(self, widget, data=None):
		print( _("About") )
	
	def delete_event(self, widget, event, data=None):
		print("delete event occurred")
		return False
	
	def destroy(self, widget, data=None):
		print("quiting app")
		self.window.hide()
		gtk.main_quit()
	
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
	
	# This while loop demonstrates how to restart a gtk app
	# The restarted app will display in the selected locale.
	restart = True
	while restart is not False:
		print ("intializing hello")
		hello = HelloWorld(localize)
		print ("calling hello.main")
		""" WARNING to gtk developers
			Why not use gtk.main() here?
			
			On ubuntu, the osd-notify (Desktop notification Specification) has a 
			hardcoded limit of 20 notifications. After that the notifications are 
			not displayed nor put into the notification queue.
			Most Python developers use pynotify for desktop notifications. pynotify is 
			too naive to handle a notification upper limit.
			So the lower level interface **dbus** is used.
			
			dbus uses:
			
			from dbus.mainloop.glib import DBusGMainLoop
			
			glib is gobject, not gtk.
			So discourage the use of both pynotify and gtk.main() to start main loop."""
		mainloop = gobject.MainLoop()
		mainloop.run()
		"""Read the flag whether or not to restart the main loop.
		Once restarted the locale strings will appear in the choosen locale."""
		print ( "hello.restart", hello.restart )
		restart = hello.restart
		del hello
