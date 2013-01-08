#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cookielib
import urllib
import urllib2
import simplejson as json
from debug import debug

class Phonty():
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        )

    def __init__(self):
        self.url = "http://phonty.com/japi/"
        self.opener.addheaders = [('User-agent', 'Phonty-Android-Client')]
        self.error = None

    def login(self, login, password):
        url = self.url + "login/"
        try:
            data = urllib.urlencode(
                                {'username': str(login),
                                 'password': str(password)})
        except:
            data = None
        request = urllib2.Request(url, data)
        response = self.send(request)
        if response == "AUTH_OK":
            return True
        else:
            self.error = response
            return False

    def balance(self,locale ="US"):
        url = self.url + "balance/"
        data = urllib.urlencode({'locale': locale})
        request = urllib2.Request(url,data)
        try:
            response = json.loads(self.send(request))["balance"]
        except KeyError,e:
            response = '0.0'
        return response

    def version(self):
        url = self.url + "version/"
        request = urllib2.Request(url)
        try:
            response = json.loads(self.send(request))["version"]
        except KeyError,e:
            response = '0.0.0'
        return response


    def direction_cost(self,phone,locale):
        url = self.url + "directioncost/"
        data = urllib.urlencode({'phone':str(phone),'locale': locale})
        request = urllib2.Request(url, data)
        try:
            response = json.loads(self.send(request))
        except KeyError,e:
            response = '0.0'
        return response

    def contacts(self):
        url = self.url + "contacts_dict/"
        request = urllib2.Request(url)
        try:
            response = json.loads(self.send(request))
        except KeyError,e:
            response = []
        return response

    def contact_delete(self, id):
        """
        Removing the contact from phonty base
        @id() - Contact id
        :rtype : bool
        """
        url = self.url + "contact_delete/"
        data = urllib.urlencode({'id': id})
        request = urllib2.Request(url, data)
        try:
            response = json.loads(self.send(request))
        except KeyError,e:
            response = {'status': "FAIL"}

        if response['status'] == "OK":
            return True
        else:
            return False

    def contact_add(self, name,phone):
        """
        Adding the contact from phonty base
        :rtype : bool
        """
        url = self.url + "contact_add/"
        data = urllib.urlencode({'name': unicode(name).encode('utf-8'), 'phone': unicode(phone).encode('utf-8')})
        request = urllib2.Request(url, data)
        try:
            response = json.loads(self.send(request))
        except KeyError,e:
            response = {'status': "FAIL"}
        try:
            self.result = int(response['status'])
            return True
        except ValueError:
            return False

    def contact_edit(self,id,name,phone):
        """
        Removing the contact from phonty base
        @id() - Contact id
        :rtype : bool
        """
        url = self.url + "contact_edit/"
        print "%s %s %s" % (id,name,phone)
        data = urllib.urlencode({'id': unicode(id).encode('utf-8'), 'name': unicode(name).encode('utf-8'), 'phone': unicode(phone).encode('utf-8')})
        request = urllib2.Request(url, data)
        try:
            response = json.loads(self.send(request))
        except KeyError,e:
            response = {'status': "FAIL"}

        if response['status'] == "OK":
            return True
        else:
            return False


    def send(self,request):
        response = None
        try:
            handle = self.opener.open(request)
            response = handle.read()

        except IOError, e:
            print 'We failed to open '
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "The error object has the following 'reason' attribute :", e.reason
                print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
        return response
