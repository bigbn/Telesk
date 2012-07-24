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

from forms.core import Core
from PyQt4 import QtCore, QtGui
import threading
from debug import debug


class Controller(object):
    def make_call(self, num):
        if len(num) > 0:
            try:
                self.core.make_call(num)
            except Exception, e:
                QtGui.QMessageBox.critical(self.form, "Error", str(e))
            #else:
                #msg = "Calling..."
                #self.form.ui.statusbar.emit(QtCore.SIGNAL("update_text"), msg)
                #if self.form.ui.dialText.count() == self.form.ui.dialText.maxCount():
                #    self.form.ui.dialText.removeItem(0)
                #self.form.ui.dialText.insertItem(-1, num)

    def hangup_call(self):
        try:
            self.core.hangup_call(self.core.calls.current)
        except Exception, e:
            QtGui.QMessageBox.critical(self.form, "Error", str(e))

    def answer_call(self):
        try:
            self.core.answer_call(self.core.calls.current)
        except Exception, e:
            QtGui.QMessageBox.critical(self.form, "Error", str(e))
    
    def reject_call(self):
        try:
            self.core.reject_call(self.core.calls.current)
        except YassException, e:
            QtGui.QMessageBox.critical(self.form, "Error", str(e))

    def hold_call(self):
        try:
            if self.holding:
                self.form.ui.actionHold.setText("hold")
                self.holding = False
                self.core.unhold_call(self.core.calls.current)
            else:
                self.form.ui.actionHold.setText("unhold")
                self.holding = True
                self.core.hold_call(self.core.calls.current)
        except Exception, e:
            QtGui.QMessageBox.critical(self.form, "Error", str(e))
        

    #### Callback functions ###

    def call_state_cb(self, uri, state, code, reason):
        debug("call state: %s %s %s" % (uri, state, code))
        arg1 = QtCore.Q_ARG(str, uri)
        arg2 = QtCore.Q_ARG(str, state)
        arg3 = QtCore.Q_ARG(int, code)
        arg4 = QtCore.Q_ARG(str, reason)
        QtCore.QMetaObject.invokeMethod(self.form, "onStateChange", QtCore.Qt.QueuedConnection, arg1, arg2, arg3, arg4)
        return

    def regstate_cb(self, uri, code, reason):
        if code == "200":

            #self.form.tray.setIcon(self.form.connectedIcon)
            QtCore.QMetaObject.invokeMethod(self.form, "onRegister", QtCore.Qt.QueuedConnection)
        else:
            QtCore.QMetaObject.invokeMethod(self.form, "onRegisterFailed", QtCore.Qt.QueuedConnection)

    def incoming_call_cb(self, call_info, dev_error):
        #arg1 = QtCore.Q_ARG(str, call_info)
        #arg2 = QtCore.Q_ARG(str, dev_error)
        QtCore.QMetaObject.invokeMethod(self.form, "onIncomingCall", QtCore.Qt.QueuedConnection)


    def __init__(self, ui):
        self.form = ui
        try:
            self.core = Core()
            self.holding = False
            self.core.cb.set_cb_callstate(self.call_state_cb)
            self.core.cb.set_cb_regstate(self.regstate_cb)
            self.core.cb.set_cb_incoming_call(self.incoming_call_cb)
            self.core.start()
        except Exception, e:
            pass
            #import traceback
            #QtGui.QMessageBox.critical(self.form, "Error dsfdsfa", traceback.format_exc())


