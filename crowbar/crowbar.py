#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

### Crowbar: Social Networking App for Twitter
###
### Copyright (C) 2010 Henry Kroll 3rd. www.thenerdshow.com
### 
### This program is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
###tthe Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.
### 
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
###MMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
### 
### You should have received a copy of the GNU General Public License
### along with this program.  If not, see http://www.gnu.org/licenses.
"""
A social networking application for viewing and
posting status updates to Twitter.

Dependends on:
http://code.google.com/p/python-twitter/

Which also depends on:
    http://cheeseshop.python.org/pypi/simplejson
    http://github.com/simplegeo/python-oauth2 
    http://code.google.com/p/httplib2/ 

1) Install latest python-twitter from hg:
hg clone https://python-twitter.googlecode.com/hg/ python-twitter

2) Download retweet patch from:

http://code.google.com/p/python-twitter/issues/detail?can=2&q=&colspec=ID%20Type%20Status%20Priority%20Milestone%20Owner%20Summary&sort=&id=130

3) Patch

cd python-twitter

patch -p0 < ../python-twitter-retweet-3.1.patch
"""

import gtk
import re,string,twitter,htmllib,webbrowser
from twitter import os,urllib,oauth,urlparse

#~ ❤ local imports ❤ 
import dialog
#~ import testify
from htmltextview import HtmlTextView

class crowbar:
    """
    Class for viewing and posting Twitter status updates.
    """
    def get_username(self):
        """Get the user login name"""
        cachedir = self.get_cachedir()
        names = os.listdir(cachedir)
        names = [a[:-5] for a in names if a[-5:]=='.auth']
        me = dialog.select('Twitter username?','Login:',None,names)  
        return me.strip()
    
    def authorize(self):
        """Twitter authorization
        
        Please put in your own consumer_key
        and consumer_secret. Ours may deactivate.
        """
        self.consumer_key = 't42Eq9aoZWuOCQEvhrTe9A'
        self.consumer_secret = 'xVrGA1o0njIwtTtuw0n4GAhmfvPpndMcnl6fabbDPI'
        
        me = self.get_username()
        
        # load cached authorization file
        cachedir = self.get_cachedir()
        cachefile = cachedir+me+'.auth'
        if os.path.exists(cachefile):
            with open(cachefile) as f:
                data=f.read()
                access_token = twitter.simplejson.loads(data)
                return access_token

        request_token_url = 'http://twitter.com/oauth/request_token'
        access_token_url = 'http://twitter.com/oauth/access_token'
        authorize_url = 'http://twitter.com/oauth/authorize'
        consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        client = oauth.Client(consumer)
        # Step 1: Get a request token. This is a temporary token that is used for 
        # having the user authorize an access token and to sign the request to obtain 
        # said access token.
        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])
        request_token = dict(urlparse.parse_qsl(content))
        # Step 2: Redirect to the provider. Since this is a CLI script we do not 

        url="%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
        webbrowser.open(url)
        # After the user has granted access to you, the consumer, the provider will
        # redirect you to whatever URL you have told them to redirect to. You can 
        # usually define this in the oauth_callback argument as well.
        oauth_verifier = dialog.getText('What is the pin?',gtk.MESSAGE_QUESTION,'pin:',
        'Fill out the form in the web page that pops up.\n'
        'You will be given a PIN number.\n'
        'Come back and enter that number here.').strip()

        # Step 3: Once the consumer has redirected the user back to the oauth_callback
        # URL you can request the access token the user has approved. You use the 
        # request token to sign this request. After this is done you throw away the
        # request token and use the access token returned. You should store this 
        # access token somewhere safe, like a database, for future use.
        token = oauth.Token(request_token['oauth_token'],
            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        resp, content = client.request(access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))
        data=twitter.simplejson.dumps(access_token)
        if '<error' not in data:
            with open(cachefile,'w') as f:
                f.write(data)
        return access_token
    
    def update_followers_count(self):
        """Updates the count of followers"""
        self.me = api.GetUserTimeline(count = 1,include_rts = True)[0].user
        fo=str(self.me.followers_count)
        fr=str(self.me.friends_count)
        self.window2.set_title(fr+" friends "+fo+" followers")

    def get_cachedir(self):
        """Returns the application's Cache dir:"""
        cachedir = os.path.expanduser('~/.crowbar_cache/')
        if not os.path.exists(cachedir):
            os.mkdir(cachedir)
        return cachedir
        
    def getshouts(self,s):
        """get names of people mentioned in s[].text"""
        names = []
        for a in s:
            try:
                atext = re.match("[^@]*(.*)",a.text).groups()[0]
                for b in atext.split("@")[1:]:
                    al = re.match("(\w+)",b).groups()[0].lower()
                    if al not in names:
                        names.append(al)
            except:
                pass
        return names
    
    def get_screen_names(self,s):
        """get s[].user.screen_name from search results"""
        names = []
        for a in s:
            al = a.user.screen_name.lower()
            if al not in names:
                names.append(al)
        return names
        
    def subem(self,sub):
        """sub everybody in sub"""
        global friends
        for a in sub:
            al = a.lower()
            if al not in friends:
                try:
                    api.CreateFriendship(al)
                    friends.append(al)
                except:
                    pass
    
    def gtk_main_quit(self,widget,data = None):
        gtk.main_quit()
        return False # return False destroys window.
    
    def delete_event(self,widget,data = None):
        widget.hide() # hide the window
        return True # return True does not destroy window.
    
    def link_clicked(self,view,url,type_):
        """follow a url or reply link"""
        url = url.replace('%26','&')
        url = url.replace('&amp;','&')
        print "url-clicked", url, type_
        if 'http://' not in url:
            if '@' in url:
                self.entry1.set_text(url)
            elif '#' == url[0]:
                self.comboboxentry1.child.set_text(url)
                self.search_clicked(None,self.comboboxentry1.child.get_text)
            elif '☆' in url:
                api.CreateFavorite(api.GetStatus(int(str(url).replace('☆',''))))
            elif '☞' in url:
                api.PostRetweet(int(str(url).replace('☞','')))
        else:
            #~ print 'launching browser'
            os.system('htmlview "'+url+'"')
    
    def post_update(self,widget,data = None):
        if data():
            api.PostUpdate(data())
        self.entry1.set_text('')
        return True
        
    def image_from_url(self,url,fname):
        """return a gtk.Image from url"""
        #~ cache img to speed up loading
        cachedir = self.get_cachedir()
        if url:
            ext = '.'+url[url.rindex('.')+1:].lower()
            if ext not in ['.jpg','.png']:
                ext = '.jpg'
            fname = str(fname)+ext
            cachefile = cachedir+fname
            #~ print url, cachefile
            if os.path.exists(cachefile):
                #~ print 'cache hit: '+cachefile
                pb = gtk.gdk.pixbuf_new_from_file(cachefile)
                pbs = pb.scale_simple(48,48,0)
                return gtk.image_new_from_pixbuf(pbs)
            fp = urllib.urlopen(url)
            pbl = gtk.gdk.PixbufLoader()
            data = fp.read()
            #~ read url into pixbuf
            if pbl.write(data):
                pb = pbl.get_pixbuf()
                try:
                    pbs = pb.scale_simple(48,48,0)
                except:
                    try:
                        fp.close()
                        pbl.close()
                    except:
                        pass
                    print 'could not scale image for', fname
                    return gtk.image_new_from_file('blank.jpg')
                    #~ pbs = pb
                #~ create image from pixbuf
                image = gtk.Image()
                image.set_from_pixbuf(pbs)
                #~ save cached copy
                if ext != '.png':
                    pb.save(cachefile,"jpeg")
                else:
                    pb.save(cachefile,"png")
                try:
                    pbl.close()
                except:
                    print url,'truncated or incomplete.'
            else:
                #~ todo: make this a broken image
                print 'broken image for',fname
                image = gtk.image_new_from_file('blank.jpg')
            fp.close()
        else:
            print 'no url for image',fname
            image = gtk.image_new_from_file('blank.jpg')
        return image
        
    def escape(self,s):
        s = s.replace('&','&amp;')
        s = s.replace('<','&lt;')
        s = s.replace('>','&gt;')
        #~ s = s.replace('"','&quot;')
        return s
    def unescape(self,s):
        p = htmllib.HTMLParser(None)
        p.save_bgn()
        p.feed(str(s))
        s = p.save_end()
        #~ s = s.replace('&lt;','<')
        #~ s = s.replace('&gt;','>')
        s = s.replace(' rel="nofollow"','')
        #~ s = s.replace('&quote;','"')
        s = s.replace('&','%26')
        s = s.replace('[1]','')
        return s
    def process_urls(self,s):
        s = self.escape(s)
        s = re.sub("(http://[^ ]+)",
                lambda m: "<a href='%s'>%s</a>" % 
                (m.group(1).replace('&amp;','&'),
                 m.group(1).replace('&amp;','&')),s)
        s = re.sub("(@)(\w+)",
                lambda m: "%s<a href='%s'>%s</a>" % 
                (m.group(1),'http://twitter.com/'+m.group(2),m.group(2)),s)
        s = re.sub("(#)(\w+)",
                lambda m: "%s<a href='%s'>%s</a>" % 
                (m.group(1),'#'+m.group(2),m.group(2)),s)
        return s

    def html_view(self,s):
        """show timeline or search data in htmlview"""
        # clear, add viewport & scrolling table
        if self.sw1.get_child() is self.html:
            self.sw1.remove(self.html)
            self.sw1.set_property("hscrollbar-policy",gtk.POLICY_NEVER)
            self.viewport1 = gtk.Viewport()
            self.sw1.add(self.viewport1)
        else:
            self.viewport1.remove(self.table1)
        self.table1 = gtk.Table(23,2,False)
        self.table1.set_row_spacings(2)
        self.table1.set_col_spacings(2)
        self.viewport1.add(self.table1)
        self.pic = []
        self.msg = []
        t = ['']
        rows = 0
        #display each user pic and instant message
        for x in s:
            user = x.GetUser()
            img = user.GetProfileImageUrl()
            usn = str(user.GetScreenName())
            t[0] = x
            reply = usn
            shouts = self.getshouts(t)
            star = '☆'
            if x.favorited:
                star = '★'
            if shouts:
                reply+=' @'+string.join(self.getshouts(t),' @')
            self.pic.append(self.image_from_url(img,usn))
            text = self.process_urls(str(x.text))
            #~ \w=\$\?\-\.\+\!\*\'\(\)/
            self.msg.append(HtmlTextView())
            self.msg[rows].connect("url-clicked",self.link_clicked)
            h = '<span style="background-color:black">' +'<a href="'+star+str(x.id)+'">'+star +'</a><span style="font-weight: bold">'+'<a href="http://twitter.com/'+usn+'">' +usn+'</a></span>: '+ text +'<br /><span style="font-size:small">' +x.relative_created_at+' via '+self.unescape(x.source)+' | <a href="@'+reply+'">reply</a> | <a href="☞' +str(x.id)+'">retweet</a></span></span>'
            try:
                self.msg[rows].display_html(str(h))
            except:
                print 'Error displaying',type(h)
                print h+'\n'
            self.table1.attach(self.pic[rows],0,1,rows,rows+1)
            self.table1.attach(self.msg[rows],1,2,rows,rows+1)
            rows+=1
        #~ self.table1.attach(self.html,0,2,rows,rows+2)
        self.blank = gtk.Label()
        self.blank.set_property('height-request',100)
        self.table1.attach(self.blank,0,2,rows,rows+2)
        #~ self.table1.set_property("border-width", 5)
        self.sw1.show_all()
    
    def initialize_window(self):
        """Show the intro page"""
        self.html = HtmlTextView()
        self.html.connect("url-clicked",self.link_clicked)
        self.html.display_html('<div><span style="color: red; text-decoration:underline">Welcome to</span><br/>\n'
                          '  <img src="http://comptune.com/images/penguin5.gif" alt="penguin" height="48" width="48" /><br/>\n'
                          '  <span style="font-size: 500%; font-family: serif">crowbar</span>\n'
                          '</div>\n')
        self.sw1.add(self.html)
        #~ add a search comboboxentry1 and 3 buttons
        self.liststore1 = gtk.ListStore(str)
        self.comboboxentry1 = gtk.ComboBoxEntry(self.liststore1, 0)
        popular = ['#teamfollowback','#tfb','#f4f']
        trending=api.GetTrendsCurrent()        
        trends = [x.name for x in trending]
        for row in popular:
            self.liststore1.append([row])
        for row in trends:
            self.liststore1.append([row])
        self.button3 = gtk.Button()
        self.button3.set_label('search')
        self.button3.set_property('width-request',55)
        self.button3.connect('clicked',self.search_clicked,self.comboboxentry1.child.get_text)
        self.button4 = gtk.Button()
        self.button4.set_label('timeline')
        self.button4.set_property('width-request',65)
        self.button4.connect('clicked',self.timeline_clicked,self.comboboxentry1.child.get_text)  
        self.button5 = gtk.Button()
        self.button5.set_label('mentions')
        self.button5.set_property('width-request',65)
        self.button5.connect('clicked',self.mentions_clicked,self.comboboxentry1.child.get_text)

        self.hbox2 = gtk.HBox(homogeneous = False)
        self.hbox2.pack_start(self.comboboxentry1)
        self.hbox2.pack_start(self.button3,expand = False,fill = True)
        self.hbox2.pack_start(self.button4,expand = False,fill = True)
        self.hbox2.pack_start(self.button5,expand = False,fill = True)
        #~ testify.test(self)
        self.vbox1.pack_start(self.hbox2,expand = False)
        self.html.show_all()
        self.hbox2.show_all()
        
    def display_results(self,s,getnames):
        """display results of searches and timelines"""
        lnames = ''
        if getnames:
            snames = self.get_screen_names(s)
            lnames = "@"+string.join(snames," @")
        shouts = self.getshouts(s)
        self.textview1.set_wrap_mode(gtk.WRAP_WORD)
        buf = self.textview1.get_buffer()
        buf.set_text(lnames+"@"+string.join(shouts," @"))        
        self.html_view(s)
        self.window2.show_all()

    def get_list(self,widget):
        it = widget.get_iter('0')
        data = []
        while 1:
            try:
                data.append(widget.get_value(it,0))
                it = widget.iter_next(it)
            except:
                return data

    def update_search(self,text):
        l = self.get_list(self.liststore1)
        if text not in l:
            self.liststore1.append([text])

    def search_clicked(self,widget,method = None):
        """get names and shouts from api search and display them"""
        text = method()
        s = api.GetSearch(text)
        self.display_results(s,True)
        self.last_action = self.search_clicked
        self.last_method = method
        self.update_search(text)
        self.update_followers_count()
        
    def timeline_clicked(self,widget,method = None):
        """get friends' timeline"""
        text = method()
        getnames = False
        if text:
            getnames = True
            if '#' in text:
                getmames = False
                text = None
        s = api.GetFriendsTimeline(text)
        self.display_results(s,getnames)
        self.last_action = self.timeline_clicked
        self.last_method = method
        self.update_search(text)
        self.update_followers_count()
        
    def mentions_clicked(self,widget,method = None):
        """get mentions"""
        s = api.GetMentions()
        self.display_results(s,True)
        self.last_action = self.mentions_clicked
        self.last_method = method
        self.update_followers_count()
        
    def refresh_clicked(self,widget,method = None):
        self.liststore1.clear()
        popular = ['#teamfollowback','#tfb','#f4f']
        trending=api.GetTrendsCurrent()        
        trends = [x.name for x in trending]
        for row in popular:
            self.liststore1.append([row])
        for row in trends:
            self.liststore1.append([row])
        self.last_action(None,self.last_method)

    def get_friendIDs(self):
        """Get friend and follower IDs"""
        global friendIDs,followerIDs
        if not globals().has_key('friendIDs'):
            print 'getting friends list...'
            try:
                friendIDs=api.GetFriendIDs()['ids']
            except:
                print ("User not properly authenticated. Will not be able to post updates.")
                return False
        if not globals().has_key('followerIDs'):
            print 'getting list of followers...'
            followerIDs=api.GetFollowerIDs()['ids']
        return True

    def follow_clicked(self,widget,data = None):
        """follow all poeple in textview1 by name"""
        if self.warn and (not dialog.ok("Are you sure?\n"
            "Following too many people may violate TOS.")):
            return
        else:
            self.warn=False
        global friends
        if not self.get_friendIDs():
            return
        buf = self.textview1.get_buffer()
        #~ iterate through the text buffer
        (iter_first, iter_last) = buf.get_bounds()
        text = buf.get_text(iter_first, iter_last)
        #~ remove spaces and build a list to follow
        text = text.replace(' ','')
        fol = []
        for x in text.split('@')[1:]:
            if x not in fol:
                fol.append(x)
        #~ friend everybody in list
        for a in fol:
            if x not in friends:
                try:
                    api.CreateFriendship(a)
                    print 'followed', a
                except:
                    print 'can not follow',a
                #~ only attempt to follow once
                friends.append(a)
        
    def follow_followers(self,widget,data = None):
        """follow followers by id not by name"""
        global friendIDs,followerIDs
        if not self.get_friendIDs():
            return
        #~ safety feature in case twitter f's up
        if len(friendIDs) < 1000:
            print 'not enough friends'
            return
        for a in followerIDs:
            if a not in friendIDs:
                try:
                    ret = api.CreateFriendship(a)
                    print 'followed',a
                except:
                    print 'could not follow',a
                #~ add to internal friends list anyway
                #~ so we don't keep trying to follow them
                friendIDs.append(a)

    def unfollow_non_followers(self,widget,data = None):
        """unfollow everybody who is not following me
        
        todo: add safelist"""
        if not self.get_friendIDs():
            return
        unsub = []
        #~ safety feature in case twitter f's up
        if len(followerIDs) < 1000:
            print 'not enough followers'
            return
        for a in friendIDs:
            if a not in followerIDs:
                unsub.append(a)
        #~ print unsub
        unsub.remove(self.me.id)
        if dialog.ok('Unfriend all '+str(len(unsub))+' non-followers?\n'
            'Abusing this may violate TOS.'):
            #UNSUB EVERYBODY IN unsub
            for a in unsub:
                try:
                    api.DestroyFriendship(a)
                    # leave on internal friends list so we don't re-follow
                    print 'unfriended',a
                except:
                    pass

    def __init__(self):
        """main initialization routine"""
        global api,friendIDs,friends
        friends=[]
        tok=self.authorize()
        self.warn=True
        api = twitter.Api(self.consumer_key,self.consumer_secret,
        tok['oauth_token'],tok['oauth_token_secret'])

        builder = gtk.Builder()
        builder.add_from_file("crowbar.glade") 

        self.window1 = builder.get_object("window1")
        self.vbox1 = builder.get_object("vbox1")
        self.sw1 = builder.get_object("sw1")
        self.window2 = builder.get_object("window2")
        self.textview1 = builder.get_object("textview1")
        self.entry1 = builder.get_object("entry1")
        self.button1 = builder.get_object("button1")
        
        builder.connect_signals(self)
        self.window2.connect("delete-event",self.delete_event)
        self.button1.connect("clicked",self.post_update,self.entry1.get_text)
        self.update_followers_count()
        self.window1.set_title("Crowbar @"+self.me.screen_name)
        self.initialize_window()
        #~ some variables to remember what we did last
        self.last_action = None
        self.last_method = None
        
if __name__ == "__main__":
    crowbar = crowbar()
    crowbar.window1.show()
    gtk.main()
