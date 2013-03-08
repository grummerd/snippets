#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Switch between gettext locales on the fly
	docs.python.org/2/library/userdit.html#module-UserDict.DictMixin
	docs.python.org/2/library/collections.html#collections.MutableMapping
"""

from __future__ import print_function
import sys, gettext
import locale, glob, os.path
import collections

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
