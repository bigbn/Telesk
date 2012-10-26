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

import threading
from japi.japi import Phonty
from PyQt4 import QtCore, QtGui
from forms.customWidgets import ClearLineEdit
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialWindow(object):
    def setupUi(self, DialWindow):
        self.phonty = Phonty()
        #interface
        DialWindow.setObjectName(_fromUtf8("DialWindow"))
        DialWindow.resize(350, 70)
        self.setMaximumWidth(350)
        self.setMaximumHeight(70)
        self.setWindowIcon(QtGui.QIcon('images/telesk.png'))
        self.baseLayout = QtGui.QVBoxLayout(DialWindow)
        self.top_spacer = QtGui.QSpacerItem(40,
                                        50,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum)
        self.baseLayout.addItem(self.top_spacer)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        #phonty items
        self.balance_label = QtGui.QLabel(self)
        self.balance_label.setText(u"Your balance is 0.0 USD")
        self.baseLayout.addWidget(self.balance_label)

        # call process
        font = QtGui.QFont()
        font.setPointSize(8)
        self.processLayout = QtGui.QVBoxLayout()

        self.callerIDLabel = QtGui.QLabel(self)
        self.callerIDLabel.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        self.callerIDLabel.setFont(font)
        self.callerIDLabel.setObjectName(_fromUtf8("callerIDLabel"))
        self.callerIDLabel.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.seconds = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.onTimer)

        self.timerLabel = QtGui.QLabel(self)
        self.timerLabel.setText(u"0:00")
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.processLayout.addWidget(self.callerIDLabel)
        self.processLayout.addWidget(self.timerLabel)


        self.hangupButton = QtGui.QToolButton(DialWindow)
        self.hangupButton.setMinimumSize(QtCore.QSize(0, 36))
        self.hangupButton.setStyleSheet(_fromUtf8(""))
        self.hangupButton.setIconSize(QtCore.QSize(36, 36))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/hangup.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hangupButton.setIcon(icon)

        self.horizontalLayout.addLayout(self.processLayout)
        self.horizontalLayout.addWidget(self.hangupButton)

        self.timerLabel.hide()
        self.callerIDLabel.hide()
        self.hangupButton.hide()

        #start form
        font = QtGui.QFont()
        font.setPointSize(18)
        self.numberEdit = ClearLineEdit()

        self.numberEdit.setFont(font)
        self.numberEdit.setObjectName(_fromUtf8("numberEdit"))
        self.horizontalLayout.addWidget(self.numberEdit)


        self.dialButton = QtGui.QToolButton(DialWindow)
        self.dialButton.setMinimumSize(QtCore.QSize(0, 36))
        self.dialButton.setStyleSheet(_fromUtf8(""))
        icon = QtGui.QIcon()

        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/call.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dialButton.setIcon(icon)

        self.dialButton.setIconSize(QtCore.QSize(36, 36))
        self.dialButton.setObjectName(_fromUtf8("dialButton"))
        self.horizontalLayout.addWidget(self.dialButton)

        #incoming
        self.incomingLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("incomingLayout"))
        self.answerButton = QtGui.QPushButton(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/call.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.answerButton.setIcon(icon)
        self.answerButton.setObjectName(_fromUtf8("answerButton"))
        self.incomingLayout.addWidget(self.answerButton)
        self.rejectButton = QtGui.QPushButton(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rejectButton.setIcon(icon1)
        self.rejectButton.setObjectName(_fromUtf8("rejectButton"))
        self.incomingLayout.addWidget(self.rejectButton)
        self.processLayout.addLayout(self.incomingLayout)
        self.rejectButton.hide()
        self.answerButton.hide()

        self.baseLayout.addLayout(self.horizontalLayout)

        #phonty elements
        self.direction_cost_label = QtGui.QLabel(self)
        self.direction_cost_label.setText(u" ")
        font = QtGui.QFont()
        font.setPointSize(8)
        self.direction_cost_label.setFont(font)
        self.baseLayout.addWidget(self.direction_cost_label)

        self.retranslateUi(DialWindow)
        QtCore.QMetaObject.connectSlotsByName(DialWindow)
        self.numberEdit.textChanged.connect(self.async_direction_cost)
        
        #login
        self.v_base_lay = self.baseLayout
        self.h_main_lay = QtGui.QHBoxLayout()

        movie = QtGui.QMovie(":/loader.gif")
        self.loader = QtGui.QLabel()
        self.loader.setMovie(movie)
        self.loader.setStyleSheet("padding: 5px")
        self.loader.setVisible(False)
        movie.start()

        self.loader.setAlignment(QtCore.Qt.AlignRight)

        self.v_base_lay.addWidget(self.loader)

        self.v_base_lay.addLayout(self.h_main_lay)

        self.v_account_lay = QtGui.QVBoxLayout()
        self.h_main_lay.addLayout(self.v_account_lay)

        self.login_label = QtGui.QLabel()
        self.login_label.setText("Login")
        self.v_account_lay.addWidget(self.login_label)
        self.login_edit = ClearLineEdit()
        self.v_account_lay.addWidget(self.login_edit)

        self.password_label = QtGui.QLabel()
        self.password_label.setText("Password")
        self.v_account_lay.addWidget(self.password_label)
        self.password_edit = QtGui.QLineEdit()
        self.password_edit.setEchoMode(QtGui.QLineEdit.Password)
        self.v_account_lay.addWidget(self.password_edit)

        self.remember_password_check = QtGui.QCheckBox()
        self.remember_password_check.setText("Remember password")
        self.v_account_lay.addWidget(self.remember_password_check)

        self.h_buttons_lay = QtGui.QHBoxLayout()
        self.v_base_lay.addLayout(self.h_buttons_lay)

        self.register_button = QtGui.QPushButton()
        self.register_button.setText("Sign Up")
        self.h_buttons_lay.addWidget(self.register_button)

        self.login_button = QtGui.QPushButton()
        self.login_button.setText("Sign In")
        self.h_buttons_lay.addWidget(self.login_button)

    def get_balance(self):
        self.balance_label.setText(_("Your balance is ")+self.phonty.balance())

    def async_direction_cost(self,number):
        thread = threading.Thread(target = self.get_direction_cost, args = (number,) )
        thread.start()

    def get_direction_cost(self,number):
        price = self.phonty.direction_cost(number,"EN")
        self.direction_cost_label.setText("%s - %s: %s per minute" % (price["country"], price["provider"], price["amount"]))

    def retranslateUi(self, DialWindow):
        DialWindow.setWindowTitle(QtGui.QApplication.translate("DialWindow", "Telesk", None, QtGui.QApplication.UnicodeUTF8))
        self.dialButton.setText(QtGui.QApplication.translate("DialWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.answerButton.setText(QtGui.QApplication.translate("CallInDialog",_("Answer"), None, QtGui.QApplication.UnicodeUTF8))
        self.rejectButton.setText(QtGui.QApplication.translate("CallInDialog",_("Reject"), None, QtGui.QApplication.UnicodeUTF8))

    def onTimer(self):
        self.seconds += 1
        m, s = divmod(self.seconds, 60)
        if m > 60:
            h, m = divmod(m, 60)
            timerText = u"%d:%02d:%02d" % (h,m,s)
        else:
            timerText = u"%d:%02d" % (m,s)
        self.timerLabel.setText(timerText)

    def startTimer(self):
        self.seconds = 0
        self.timer.start()
