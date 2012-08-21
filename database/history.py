#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime
class HistoryAdapter():
    def __init__(self):
        self.PHONE = "phone"
        self.DATE = "date"
        self.DURATION = "duration"
        self.DIRECTION = "direction"

        self.connection = None
        self.cursor = None
        self.debug = True
        try:
            self.connection = lite.connect("history.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT SQLITE_VERSION()')

            data = self.cursor.fetchone()
            print "SQLite version: %s" % data

        except lite.Error, e:
            print "Error %s:" % e.args[0]
        self.preinit()

    def preinit(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS History(%s TEXT , %s TEXT, %s INT, %s INT)" % (self.DATE,self.PHONE, self.DURATION, self.DIRECTION ))

    def incoming(self,phone):
        date = datetime.datetime.now().strftime('%H:%M %d.%m')
        sql = 'INSERT INTO History VALUES("%s","%s","0","1");' % (date,phone)
        print sql
        self.cursor.execute(sql)
        self.connection.commit()

    def outgoing(self,phone):
        date = datetime.datetime.now().strftime('%H:%M %d.%m')
        sql = 'INSERT INTO History VALUES("%s","%s","0","0");' % (date,phone)
        print sql
        self.cursor.execute(sql)
        self.connection.commit()

    def list(self):
        sql = 'SELECT * FROM History'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        if self.connection:
            self.connection.close()
