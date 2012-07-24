# -*- coding: utf-8 -*-

# Copyright (C) 2010-2012 SKAT Ltd. (http://www.scat.su)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(461, 173)
        self.verticalLayout = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(SettingsDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.serverEdit = QtGui.QLineEdit(self.tab)
        self.serverEdit.setObjectName(_fromUtf8("serverEdit"))
        self.gridLayout.addWidget(self.serverEdit, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.portEdit = QtGui.QLineEdit(self.tab)
        self.portEdit.setObjectName(_fromUtf8("portEdit"))
        self.gridLayout.addWidget(self.portEdit, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.loginEdit = QtGui.QLineEdit(self.tab)
        self.loginEdit.setObjectName(_fromUtf8("loginEdit"))
        self.gridLayout.addWidget(self.loginEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 2, 1, 1)
        self.passwordEdit = QtGui.QLineEdit(self.tab)
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.gridLayout.addWidget(self.passwordEdit, 1, 3, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 37, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.aaCheckBox = QtGui.QCheckBox(self.tab_2)
        self.aaCheckBox.setObjectName(_fromUtf8("aaCheckBox"))
        self.verticalLayout_4.addWidget(self.aaCheckBox)
        self.aotCheckBox = QtGui.QCheckBox(self.tab_2)
        self.aotCheckBox.setObjectName(_fromUtf8("aotCheckBox"))
        self.verticalLayout_4.addWidget(self.aotCheckBox)
        self.ustcheckBox = QtGui.QCheckBox(self.tab_2)
        self.ustcheckBox.setObjectName(_fromUtf8("ustcheckBox"))
        self.verticalLayout_4.addWidget(self.ustcheckBox)
        spacerItem1 = QtGui.QSpacerItem(20, 66, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(self.tab_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.inputComboBox = QtGui.QComboBox(self.tab_3)
        self.inputComboBox.setObjectName(_fromUtf8("inputComboBox"))
        self.gridLayout_2.addWidget(self.inputComboBox, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.outputComboBox = QtGui.QComboBox(self.tab_3)
        self.outputComboBox.setObjectName(_fromUtf8("outputComboBox"))
        self.gridLayout_2.addWidget(self.outputComboBox, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 35, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.cancelButton = QtGui.QPushButton(SettingsDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/button_cancel.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.okButton = QtGui.QPushButton(SettingsDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/button_ok.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okButton.setIcon(icon1)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SettingsDialog)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsDialog.reject)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL(_fromUtf8("clicked()")), SettingsDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle( _("Settings"))
        self.label.setText(_("SIP Server"))
        self.label_6.setText(_("Port"))
        self.portEdit.setText("5060")
        self.label_2.setText(_("Username"))
        self.label_3.setText(_("Password"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),_("SIP"))
        self.aaCheckBox.setText(_("Auto answer"))
        self.aotCheckBox.setText(_("Always on top"))
        self.ustcheckBox.setText(_("Use the system theme (restart needed)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _("Interface"))
        self.label_4.setText(_("Capture device"))
        self.label_5.setText(_("Output device"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _("Sound"))
        self.cancelButton.setText(_("Cancel"))
        self.okButton.setText(_("OK"))

import resource_rc
