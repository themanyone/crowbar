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

import gtk
def select(question,label='Select:',additional=None,data=None):
    """select(question,label='Select:',additional=None,data=None):
    
    Returns user selection from list of items in data.
    If the list is empty, reverts to a question dialog."""
    if data:
        return getText(question,gtk.MESSAGE_QUESTION,
    label,additional,gtk.ComboBoxEntry,data)
    else:
        return getText(question,gtk.MESSAGE_QUESTION,
    label,additional)
def ok(text,name='Attention'):
    """ok(text,name='Attention'):
    
    OK/Cancel Dialog with info icon"""
    dia = gtk.Dialog(name,None,gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_OK,gtk.RESPONSE_ACCEPT,gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT))
    dia.child.add(gtk.Label(text))
    dia.show_all()
    res = dia.run()
    dia.destroy()
    return (res == gtk.RESPONSE_ACCEPT)
def alert(text):
    """alert(text):
    
    Display an alert with warning icon"""
    getText(text,icon=gtk.MESSAGE_WARNING)
def info(text):
    """info(text):
    
    Displays an informational dialog"""
    getText(text,icon=gtk.MESSAGE_INFO)
def question(question,label='Enter:',additional=None):
    """question(question,label,additional=None):
    
    Asks question. Returns text from input box"""
    return getText(question,gtk.MESSAGE_QUESTION,
    name,additional)
def responseToDialog(entry, dialog, response):
    """Callback to set return value to that of dialog text    
    """
    dialog.response(response)
def getText(question,icon=0,label=None,additional=None,widget=gtk.Entry,data=None):
    """getText(question,icon=0,label=None,additional=None,
    widget=gtk.Entry,data=None):
    
    General purpose dialog overloaded and abused by all other
    methods in this class. Rather not use it but go ahead."""
    #~ q=gtk.MESSAGE_QUESTION
    dialog = gtk.MessageDialog(
        None,
        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
        icon, gtk.BUTTONS_OK,
        None)
    dialog.set_markup(question)
    #create a horizontal box to pack entry and label
    hbox = gtk.HBox()
    hbox.pack_start(gtk.Label(label), False, 5, 5)
    if label:
        #create text input field or comboboxentry
        if widget==gtk.ComboBoxEntry:
            liststore=gtk.ListStore(str)
            for row in data:
                liststore.append([row])
            entry =  widget(liststore)
            txtbox = entry.child
            txtbox.set_text(data[0])
        else:
            entry = widget()
            txtbox=entry
        #pressing enter signifies OK
        txtbox.connect("activate", responseToDialog, dialog, gtk.RESPONSE_OK)
        hbox.pack_end(entry)
    #display additional text
    dialog.format_secondary_markup(additional)
    #add it and show it
    dialog.vbox.pack_end(hbox, True, True, 0)
    dialog.show_all()
    #run dialog
    dialog.run()
    response=None
    if label:
        response = txtbox.get_text()
    dialog.destroy()
    return response

if __name__ == '__main__':
    print "The name was %s" % question('What is your name?','name:')
    #~ gtk.main()
