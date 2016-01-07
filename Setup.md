# Setting things up

# Crowbar setup #

Install dependencies
  * Python 2.7, pyGTK
  * http://code.google.com/p/python-twitter/
  * http://cheeseshop.python.org/pypi/simplejson
  * http://github.com/simplegeo/python-oauth2
  * http://code.google.com/p/httplib2/

  1. Install latest python-twitter from hg:
```
  $ hg clone https://python-twitter.googlecode.com/hg/ python-twitter
```

Download [retweet patch](http://code.google.com/p/python-twitter/issues/detail?can=2&q=&colspec=ID%20Type%20Status%20Priority%20Milestone%20Owner%20Summary&sort=&id=130).

Patch
```
  $ cd python-twitter
  $ patch -p0 < ../python-twitter-retweet-3.1.patch
```

Install python-twitter
```
  $ python setup.py build
  $ python setup.py install
```

Get Crowbar
```
  $ svn checkout http://crowbar.googlecode.com/svn/trunk/ crowbar-read-only
  $ cd trunk/crowbar
```

Examine the source with your favorite text editor. We're using scite.
```
  $ scite crowbar.py
```

Run it
```
  $ ./crowbar.py
```

Common fixes:
If authentication fails, delete [yourusername](yourusername.md).auth and try again.