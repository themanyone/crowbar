#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

### test.py: Quick test of htmlview widget
###
### Copyright (C) 2010 Henry Kroll 3rd. www.thenerdshow.com
### 
### This program is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
###the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.
### 
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
###MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
### 
### You should have received a copy of the GNU General Public License
### along with this program.  If not, see http://www.gnu.org/licenses.
import sys,gtk,urllib
from htmltextview import HtmlTextView

class test:
    """
    Displays a window and tests the htmlview widget.
    """
    def window_close(self,widget,data=None):
        gtk.main_quit()
    def __init__(self):
        w=gtk.Window()
        print (sys.getdefaultencoding())
        msg1="""<span style="background-color:black">ω&RT</span>

"""
        print type(msg1)
        htmlview = HtmlTextView()
        def url_cb(view, url, type_):
            print ("url-clicked", url, type_))
        htmlview.connect("url-clicked", url_cb)
        w.connect("delete-event",self.window_close)
        htmlview.display_html(msg1)
        w.add(htmlview)
        w.show_all()

if __name__ == "__main__":
    test=test()
    gtk.main()
