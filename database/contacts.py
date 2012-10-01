#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime
from settings_file import profile_path

class ContactsAdapter():
    def __init__(self):
        self.TABLE_NAME = "Contacts"
        self.ID = "id"
        self.NAME = "name"
        self.PHONE = "phone"

        self.connection = None
        self.cursor = None
        self.debug = True
        
        try:
            self.connection = lite.connect(profile_path("data.db"))
            self.cursor = self.connection.cursor()
            self.cursor.execute('SELECT SQLITE_VERSION()')

            data = self.cursor.fetchone()
            print "SQLite version: %s" % data

        except lite.Error, e:
            print "Error %s:" % e.args[0]
        self.preinit()

    def preinit(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.TABLE_NAME + " (_id INTEGER PRIMARY KEY AUTOINCREMENT, " + self.ID + " INTEGER , " + self.NAME + " TEXT , " + self.PHONE + " TEXT);")
        self.connection.commit()


    def clean(self):
        self.cursor.execute("DELETE FROM "+self.TABLE_NAME+";");
        self.connection.commit();

    def delete(self,id):
        self.cursor.execute("DELETE FROM "+self.TABLE_NAME+" WHERE "+self.ID+"="+id+";");
        self.connection.commit();

    def add(self,id,name,phone):
        self.cursor.execute("INSERT INTO "+self.TABLE_NAME+" ("+self.ID+","+self.NAME+","+self.PHONE+") VALUES ("+id+",'"+name+"','"+phone+"');");
        self.connection.commit();

    def edit(self,id,name,phone):
        self.cursor.execute("UPDATE "+self.TABLE_NAME+" SET "+self.NAME+"='"+name+"', "+self.PHONE+"='"+phone+"' WHERE "+self.ID+"="+id);
        self.connection.commit();

    def list(self):
        sql = 'SELECT * FROM '+self.TABLE_NAME+";";
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def close(self):
        if self.connection:
            self.connection.close()
