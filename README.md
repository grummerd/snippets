snippets
========

Great pygtk GUI apps should have a way to switch between languages "on the fly".
Issues that are resolved:

1. Switch the locale (language)

2. Tell gtk to refresh all the windows / widgets, by unfortunitely having to restart the app!

Outside of the scope of this snippet:

1. Windows / MacOS support (https://github.com/dieterv/elib.intl/blob/master/lib/elib/intl/__init__.py)

Usage
========

Edit the line:

localize = Localize(app_name="msgu")

Change the app_name to ur existing app's name. Assume you already have [app_name].mo files installed on ur system.

Change all instances of _("About"). Should be a word which is already translated in ur .mo files.
In mine, have two .mo files [ja, en].
en: About
ja: について

Then run the app:
python localize.py

Click en or ja buttons will switch the language of the gtk window. Clicking bottom button will quit the app.
