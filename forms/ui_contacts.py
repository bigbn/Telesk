# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/contacts.ui'
#
# Created: Tue Aug 21 10:09:21 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Contacts(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("ContactsForm"))
        Form.resize(400, 300)
        self.setMaximumWidth(400)
        self.setMaximumHeight(300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        #self.tab = QtGui.QWidget()

        #self.tab.setObjectName(_fromUtf8("tab"))
        #self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))


        
        self.scrollArea = QtGui.QScrollArea(self.tab_2)
        self.scrollArea.setStyleSheet("background: rgb(40,40,40); border-color: rgb(50,50,50)")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setStyleSheet("background: rgb(40,40,40); border-color: rgb(50,50,50)")
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 370, 240))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.vcallsLayout =  QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        
        self.vcallsLayout.setSpacing(0)

        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.is_hidden = true

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Contacts", None, QtGui.QApplication.UnicodeUTF8))
        #self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Form", "Contacs", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Calls history"))

