#!/usr/bin/env python

import urllib2
import threading

class MyHandler(urllib2.HTTPHandler):
    def http_response(self, req, response):
        print "url: %s" % (response.geturl(),)
        print "info: %s" % (response.info(),)
        for l in response:
            print l
        return response

o = urllib2.build_opener(MyHandler())
t = threading.Thread(target=o.open, args=('http://www.google.com/',))
t.start()
print "I'm asynchronous!"
