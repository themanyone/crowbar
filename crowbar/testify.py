#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

### testify.py: Module of Crowbar Social Networking App for Twitter
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
import time,gtk,string

class test:
    """
    A module for testing the Crowbar Social Networking Application

    Usage: Uncomment the lines with the word "testify" in them.
    """
    def init_test(self,obj):
        """Add test button to hbox2, set callback"""
        obj.button6 = gtk.Button()
        obj.button6.set_label('test')
        obj.button6.set_property('width-request',55)
        obj.button6.connect('clicked',self.test_clicked,obj)
        obj.hbox2.pack_start(obj.button6,expand = False,fill = True)

    def test_clicked(self,obj,crowbar=None):
        """simulate displaying a search and harvesting some names"""
        strings = []
        strings.append('Hello @ubuntu_linux @gnome @Linux_Kernel<<@linux_pro<><>. http://gnu.org How\'s it going?')
        strings.append('I\'m doing fine. Shout outs to>>>@gnulinux<><> #linux @Penguins')
        strings.append('Good to hear. http://www.youtube.com/watch?v=mQl212k8FUI&amp;sns=fb :)')
        strings.append('Can I get in on this? #testing @test @security')
        s = [] #create test users
        s.append(mktest('Fedora', strings[0]))
        s.append(mktest('Ubuntu_Linux', strings[1]))
        s[-1].user.profile_image_url = 'http://a1.twimg.com/profile_images/55963805/UbuntuLogo_normal.png'
        s.append(mktest('Fedora', strings[2]))
        s.append(mktest('Tester', strings[3]))
        s[-1].user.profile_image_url = 'http://comptune.com/images/compguy.jpg'
        snames = crowbar.get_screen_names(s)
        shouts = crowbar.getshouts(s)
        crowbar.textview1.set_wrap_mode(gtk.WRAP_WORD)
        buf = crowbar.textview1.get_buffer()
        buf.set_text("@"+string.join(snames," @")+"@"+string.join(shouts," @"))   
        crowbar.html_view(s)
        crowbar.window2.show_all()
        
    def __init__(self,obj):
        self.init_test(obj)

class mktest:
    """test class created to test the functions in crowbar
        
import testify
test=testify.mktest('eek')
test.user.GetDescription()
test.user.status
    """

    class user:
        def GetDescription(self):
            return self.description
        def GetFavouritesCount(self):
            return self.favourites_count
        def GetFollowersCount(self):
            return self.followers_count
        def GetFriendsCount(self):
            return self.friends_count
        def GetId(self):
            return self.id
        def GetLocation(self):
            return self.location
        def GetName(self):
            return self.name
        def GetProfileBackgroundColor(self):
            return self.profile_background_color
        def GetProfileBackgroundImageUrl(self):
            return self.profile_image_url
        def GetProfileBackgroundTile(self):
            return self.profile_background_tile
        def GetProfileImageUrl(self=None):
            return self.profile_image_url
        def GetProfileLinkColor(self):
            return self.profile_link_color
        def GetProfileSidebarFillColor(self):
            return self.profile_sidebar_fill_color
        def GetProfileTextColor(self):
            return self.profile_text_color
        def GetProtected(self):
            return self.protected
        def GetScreenName(self):
            return self.screen_name
        def GetStatus(self):
            return self.status
        def GetStatusesCount(self):
            return self.statuses_count
        def GetTimeZone(self):
            return self.time_zone
        def GetUrl(self):
            return self.url
        def GetUtcOffset(self):
            return self.utc_offset

        def SetDescription(self,text):
            self.description=text
        def SetFavouritesCount(self,num=0):
            self.favourites_count=num
        def SetFollowersCount(self,num=0):
            self.followers_count=num
        def SetFriendsCount(self,num=0):
            self.friends_count=num
        def SetId(self,num=0):
            self.id=num
        def SetLocation(self,text):
            self.location=text
        def SetName(self,text):
            self.name=text
        def SetProfileBackgroundColor(self,text):
            self.profile_background_color=text
        def SetProfileBackgroundImageUrl(self,text):
            self.profile_background_image_url=text
        def SetProfileBackgroundTile(self,boolean):
            self.profile_background_tile=boolean
        def SetProfileImageUrl(self,text):
            self.profile_image_url=text
        def SetProfileLinkColor(self,text):
            self.profile_link_color=text
        def SetProfileSidebarFillColor(self,text):
            self.profile_sidebar_fill_color=text
        def SetProfileTextColor(self,text):
            self.profile_text_color=text
        def SetProtected(self,boolean):
            self.protected=boolean
        def SetScreenName(self,text):
            self.screen_name=text
        def SetStatus(self,text):
            self.status=text
        def SetStatusesCount(self,num=0):
            self.statuses_count=num
        def SetTimeZone(self,text):
            self.time_zone=text
        def SetUrl(self,text):
            self.url=text
        def SetUtcOffset(self,text):
            self.utc_offset=text

        description = 'Very cool penguin'
        favourites_count = 4
        followers_count = 231
        friends_count = 272
        id = 0
        location='Antarctica'
        name='Percival Penguin'
        profile_background_color = 'ffffff'
        profile_background_tile = True
        profile_background_image_url = None
        profile_image_url = 'http://a3.twimg.com/profile_images/61299307/fedoralogo_normal.png'
        profile_link_color = 'f51629'
        profile_sidebar_fill_color = 'ffffff'
        profile_text_color = 'a200ff'
        protected = False
        screen_name = 'penguin5'
        statuses_count = 6401
        status='My status is totally cool.'
        time_zone = 'Vancouver'
        url = 'http://thenerdshow.com'
        utc_offset = '-28800'
    
    def GetCreatedAt(self):
        return self.created_at
    def GetCreatedAtInSeconds(self):
        return self.created_at_in_seconds
    def GetFavorited(self):
        return self.favorited
    def GetId(self):
        return self.id
    def GetInReplyToScreenName(self):
        return self.in_reply_to_screen_name
    def GetInReplyToStatusId(self):
        return self.in_reply_to_status_id
    def GetInReplyToUserId(self):
        return self.in_reply_to_user_id
    def GetLocation(self):
        return self.location
    def GetNow(self):
        return self.now
    def GetRelativeCreatedAt(self):
        return self.relative_created_at
    def GetSource(self):
        return self.source
    def GetText(self):
        return self.text
    def GetTruncated(self):
        return self.truncated
    def GetUser(self):
        return self.user

    def SetCreatedAt(self,text):
        self.created_at=text
    def SetFavorited(self,boolean=False):
        self.favorited=boolean
    def SetId(self,num):
        self.id=num
    def SetInReplyToScreenName(self,text):
        self.in_reply_to_screen_name=text
    def SetInReplyToStatusId(self,text):
        self.in_reply_to_status_id=num
    def SetInReplyToUserId(self,num):
        self.in_reply_to_user_id=num
    def SetLocation(self,text):
        self.location=text
    def SetNow(self,num):
        self.now=num
    def SetSource(self,text):
        self.source=text
    def SetText(self,text):
        self.text=text
    def SetTruncated(self,boolean=False):
        self.truncated=boolean
    def SetUser(self,user_object):
        self.user=user_object
  
    def __init__(self,name,text):
        """append data to .text"""
        self.text = text
        self.created_at = time.strftime("%a %b %d %H:%M:%S +0000 %Y", time.gmtime())
        self.now = self.created_at
        self.relative_created_at='about 1 minutes ago'
        self.favorited = False
        self.truncated = False
        self.location = None
        self.in_reply_to_user_id = None
        self.in_reply_to_status_id = None
        self.in_reply_to_screen_name = None
        self.created_at_in_seconds = time.time()
        self.source = '&lt;a href=&quot;http://thenerdshow.com&quot;&gt;crowbar&lt;/a&gt;'
        self.id = 0
        #~ bind functions in inner class
        self.user=self.user()
        self.user.screen_name = name
        #~ self=self()
        """ prevents the following error:
TypeError: unbound method GetDescription() must be called with user instance as first argument (got nothing instead) """

if __name__ == "__main__":
    test=mktest('foo','hello there!')
    print test.user.screen_name, test.text, test.relative_created_at
    