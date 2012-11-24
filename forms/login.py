# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import threading
from japi.japi import Phonty
BaseClass = QtGui.QDialog
from ui_login import Ui_Login as formClass
from dialer import Dialer

class LoginForm(formClass, BaseClass):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)
        self.phonty = Phonty()
        self.connect_signals()

    def start(self):
        self.show()
        return False

    def login(self):
        self.loader.setVisible(True)
        number = self.login_edit.text()
        password = self.password_edit.text()
        thread = threading.Thread(target=self.autorize,
                                  args=(number, password))

        thread.start()

    def autorize(self, number, password):
        if self.phonty.login(number, password):
            self.emit( QtCore.SIGNAL('auth_ok(QString)'), "auth ok" )
        else:
            self.emit( QtCore.SIGNAL('auth_wrong(QString)'), "auth wrong" )

    def register(self):
        pass

    def login_again(self):
        self.loader.setVisible(False)

    def start_dialer(self):
        self.loader.hide()
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setText("Starting. Please wait few seconds")
        self.login_edit.hide()
        self.password_label.hide()
        self.password_edit.hide()
        self.remember_password_check.hide()
        self.register_button.hide()
        self.login_button.hide()
        QtGui.qApp.processEvents()
        Dialer()
        self.hide()

    def connect_signals(self):
        self.connect( self, QtCore.SIGNAL("auth_ok(QString)"), self.start_dialer )
        self.connect( self, QtCore.SIGNAL("auth_wrong(QString)"), self.login_again )

        self.connect(self.login_button,
                     QtCore.SIGNAL("clicked()"),
                     self.login)

        self.connect(self.register_button,
                     QtCore.SIGNAL("returnPressed()"),
                     self.register)
