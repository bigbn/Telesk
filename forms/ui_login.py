# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from customWidgets import ClearLineEdit

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Login(object):
    def setupUi(self, Form):
        style = """QDialog {background: white url(:/phonty.png) no-repeat top left}
                    QLabel {color: #555555;}"""
        Form.setObjectName(_fromUtf8("LoginForm"))
        Form.resize(485, 300)
        Form.setWindowTitle(_("Phonty"))
        self.setStyleSheet(style)

        self.v_base_lay = QtGui.QVBoxLayout(self)
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

        self.top_spacer = QtGui.QSpacerItem(40,
                                        50,
                                        QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum)
        self.v_account_lay.addItem(self.top_spacer)

        self.login_label = QtGui.QLabel()
        self.login_label.setText(_("Username"))
        self.v_account_lay.addWidget(self.login_label)
        self.login_edit = ClearLineEdit()
        self.v_account_lay.addWidget(self.login_edit)

        self.password_label = QtGui.QLabel()
        self.password_label.setText(_("Password"))
        self.v_account_lay.addWidget(self.password_label)
        self.password_edit = QtGui.QLineEdit()
        self.v_account_lay.addWidget(self.password_edit)

        self.remember_password_check = QtGui.QCheckBox()
        self.remember_password_check.setText(_("Remember password"))
        self.v_account_lay.addWidget(self.remember_password_check)

        self.h_buttons_lay = QtGui.QHBoxLayout()
        self.v_base_lay.addLayout(self.h_buttons_lay)

        self.register_button = QtGui.QPushButton()
        self.register_button.setText(_("Sign Up"))
        self.h_buttons_lay.addWidget(self.register_button)

        self.login_button = QtGui.QPushButton()
        self.login_button.setText(_("Sign In"))
        self.h_buttons_lay.addWidget(self.login_button)

        self.setMaximumWidth(400)
        self.setMaximumHeight(240)