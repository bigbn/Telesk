#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from japi.japi import Phonty

__author__ = 'bigbn'

class JapiTests(TestCase):
    phonty = Phonty()

    def login(self):
        self.phonty.login("79127574956","iafzo7")

    def test_lonin_empty(self):
        self.assertFalse(self.phonty.login(None,None))

    def test_balance(self):
        self.login()
        self.assertNotEquals("0.0", self.phonty.balance())

    def test_balance_wrong_locale(self):
        cases = (None, 0, 10, -1, [], ",mgjhg;''")
        for case in cases:
            self.assertEqual('0.0',self.phonty.balance(locale=case))

        self.login()
        for case in cases:
            self.assertNotEquals('0.0',self.phonty.balance(locale=case))

    def test_balance_right(self):
        cases = ("RU","EN")
        for case in cases:
            self.assertEquals("0.0", self.phonty.balance(locale=case))

        self.login()
        for case in cases:
            self.assertNotEquals("0.0", self.phonty.balance(locale=case))

    #todo: logout; ovverrides self.close()