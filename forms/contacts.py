from PyQt4 import QtCore, QtGui
BaseClass = QtGui.QDialog
from ui_contacts import Ui_Contacts as formClass
import sys
from debug import debug
import os
from StringIO import StringIO

class ContactsForm(formClass, BaseClass):
    def __init__(self,  parent=None):
        super(ContactsForm, self).__init__(parent,QtCore.Qt.FramelessWindowHint)
        self.setupUi(self)
        self.setStyleSheet("""
                              QDialog {background-color: rgb(30,30,30); color: rgb(255,255,255); border-style: outset; border-width: 1px;
                                         border-color: rgb(50,50,50);
}
                              QLabel {color: rgb(255,255,255);}
                              QTabWidget::pane { border-top: 0px solid #C2C7CB; }
                               QTabBar::tab { background-color: rgb(30,30,30); color: white; font-weight: bold}

                              """)


    def fillHistory(self):
        pass

